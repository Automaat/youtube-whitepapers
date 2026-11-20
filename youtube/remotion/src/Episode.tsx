import type { FC } from "react";
import { AbsoluteFill, Audio, Freeze, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { ChapterCard, Chrome, OutroCard, TitleCard } from "./design/cards";
import { SANS } from "./design/fonts";
import { Serif, Text } from "./design/ui";
import { SceneContext, type SceneInfo } from "./design/scene";
import { ThemeContext, useTheme } from "./design/theme";
import { THEMES } from "./design/tokens";
import { EPISODES } from "./episodes/registry";
import type { Timeline, TimelineScene } from "./timeline";

const CHAPTER_CARD_SECONDS = 2.5;

const MissingScene = ({ id }: { id: string }) => {
  const t = useTheme();
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontFamily: SANS, fontSize: 40, color: t.danger }}>
      Brak sceny: {id}
    </AbsoluteFill>
  );
};

const sceneInfo = (tl: Timeline, scene: TimelineScene): SceneInfo => {
  const f = (s: number) => Math.round((s - scene.start) * tl.fps);
  return {
    id: scene.id,
    duration: Math.max(1, Math.round((scene.end - scene.start) * tl.fps)),
    cues: Object.fromEntries(Object.entries(scene.cues).map(([k, v]) => [k, f(v)])),
    speakers: tl.segments
      .filter((s) => s.scene === scene.id)
      .map((s) => ({ speaker: s.speaker, from: f(s.start), to: f(s.end) })),
  };
};

const ChromeLayer = ({ tl }: { tl: Timeline }) => {
  const frame = useCurrentFrame();
  const sec = frame / tl.fps;
  const scene = tl.scenes.find((s) => sec >= s.start && sec < s.end);
  if (!scene || scene === tl.scenes[0] || sec >= tl.audioSeconds) return null;
  const seg = tl.segments.find((s) => sec >= s.start && sec < s.end);
  const prev = [...tl.segments].reverse().find((s) => s.start <= sec);
  return (
    <Chrome
      number={tl.number}
      title={tl.title}
      chapters={tl.chapters}
      chapterIndex={tl.chapters.findIndex((c) => c.id === scene.chapter)}
      speaker={(seg ?? prev)?.speaker ?? "narrator"}
    />
  );
};

export const Episode: FC<Timeline> = (tl) => {
  const theme = THEMES[tl.theme];
  const fps = tl.fps;
  const sceneMap = EPISODES[tl.slug] ?? {};
  const introFrames = Math.round(tl.introSeconds * fps);
  const audioFrames = Math.round(tl.audioSeconds * fps);
  const chapterStarts = tl.chapters
    .map((c, index) => ({ index, scene: tl.scenes.find((s) => s.chapter === c.id) }))
    .filter((c) => c.scene !== undefined);

  return (
    <ThemeContext.Provider value={theme}>
      <AbsoluteFill style={{ background: theme.canvas }}>
        {tl.audio ? <Audio src={staticFile(tl.audio)} /> : null}
        {tl.scenes.map((scene) => {
          const from = Math.round(scene.start * fps);
          const dur = Math.max(1, Math.round(scene.end * fps) - from);
          const Scene = sceneMap[scene.id];
          return (
            <Sequence key={scene.id} from={from} durationInFrames={dur} name={scene.id}>
              <SceneContext.Provider value={sceneInfo(tl, scene)}>
                {Scene ? <Scene /> : <MissingScene id={scene.id} />}
              </SceneContext.Provider>
            </Sequence>
          );
        })}
        <ChromeLayer tl={tl} />
        {chapterStarts.map(({ index, scene }) => (
          <Sequence key={`chapter-${index}`} from={Math.max(introFrames, Math.round(scene!.start * fps))} durationInFrames={Math.round(CHAPTER_CARD_SECONDS * fps)} name={`chapter-${index + 1}`}>
            <ChapterCard chapters={tl.chapters} index={index} />
          </Sequence>
        ))}
        <Sequence from={0} durationInFrames={introFrames} name="intro">
          {tl.thumbnail ? (
            <Img src={staticFile(tl.thumbnail)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          ) : (
            <ThumbnailCard tl={tl} intro />
          )}
        </Sequence>
        <Sequence from={audioFrames} durationInFrames={Math.round(tl.outroSeconds * fps)} name="outro">
          <OutroCard />
        </Sequence>
      </AbsoluteFill>
    </ThemeContext.Provider>
  );
};

const ART_BOX = { x: 980, y: 110, w: 860, h: 860 };
const ART_HOLD_SECONDS = 1.5;

const termSize = (term: string) => (term.length <= 5 ? 260 : term.length <= 8 ? 200 : 150);

/** Template A from docs/research/2026-11-youtube-thumbnails.md: big term + one diagram. */
const ThumbnailCard = ({ tl, intro = false }: { tl: Timeline; intro?: boolean }) => {
  const t = useTheme();
  const art = tl.thumbnailArt;
  const scene = art ? tl.scenes.find((s) => s.id === art.scene) : undefined;
  const Scene = art ? EPISODES[tl.slug]?.[art.scene] : undefined;
  if (!art || !scene || !Scene) {
    return <TitleCard number={tl.number} title={tl.title} subtitle={tl.subtitle} authors={tl.authors} at={intro ? 0 : -60} />;
  }
  const info = sceneInfo(tl, scene);
  const frame = Math.min(info.duration - 1, (info.cues[art.cue] ?? 0) + Math.round(ART_HOLD_SECONDS * tl.fps));
  const [cx, cy, cw, ch] = art.crop ?? [0, 0, 1920, 1080];
  const scale = Math.min(ART_BOX.w / cw, ART_BOX.h / ch);
  const w = cw * scale;
  const h = ch * scale;
  return (
    <AbsoluteFill style={{ background: t.canvas }}>
      <div style={{ position: "absolute", left: ART_BOX.x + (ART_BOX.w - w) / 2, top: ART_BOX.y + (ART_BOX.h - h) / 2, width: w, height: h, overflow: "hidden", borderRadius: 28, border: `3px solid ${t.line}`, background: t.canvas }}>
        <div style={{ position: "absolute", width: 1920, height: 1080, transform: `scale(${scale}) translate(${-cx}px, ${-cy}px)`, transformOrigin: "0 0" }}>
          <SceneContext.Provider value={info}>
            <Freeze frame={frame}>
              <Scene />
            </Freeze>
          </SceneContext.Provider>
        </div>
      </div>
      <div style={{ position: "absolute", left: 120, top: 0, bottom: 0, width: 780, display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <Text size={34} weight={700} color={t.muted} style={{ letterSpacing: "0.14em", textTransform: "uppercase" }}>
          Głęboki Odczyt
        </Text>
        <Serif size={termSize(art.term)} style={{ lineHeight: 0.95, margin: "20px 0 28px" }}>
          {art.term}
        </Serif>
        {art.tagline ? (
          <Text size={64} weight={700} style={{ lineHeight: 1.15 }}>
            {art.tagline}
          </Text>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

export const Thumbnail: FC<Timeline> = (tl) => (
  <ThemeContext.Provider value={THEMES[tl.theme]}>
    <ThumbnailCard tl={tl} />
  </ThemeContext.Provider>
);

export const Outro: FC<Timeline> = (tl) => (
  <ThemeContext.Provider value={THEMES[tl.theme]}>
    <OutroCard />
  </ThemeContext.Provider>
);
