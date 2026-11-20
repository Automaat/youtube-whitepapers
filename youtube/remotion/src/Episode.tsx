import type { FC } from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { ChapterCard, Chrome, OutroCard, TitleCard } from "./design/cards";
import { SANS } from "./design/fonts";
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
            <TitleCard number={tl.number} title={tl.title} subtitle={tl.subtitle} authors={tl.authors} />
          )}
        </Sequence>
        <Sequence from={audioFrames} durationInFrames={Math.round(tl.outroSeconds * fps)} name="outro">
          <OutroCard />
        </Sequence>
      </AbsoluteFill>
    </ThemeContext.Provider>
  );
};

export const Thumbnail: FC<Timeline> = (tl) => (
  <ThemeContext.Provider value={THEMES[tl.theme]}>
    <TitleCard number={tl.number} title={tl.title} subtitle={tl.subtitle} authors={tl.authors} at={-60} />
  </ThemeContext.Provider>
);

export const Outro: FC<Timeline> = (tl) => (
  <ThemeContext.Provider value={THEMES[tl.theme]}>
    <OutroCard />
  </ThemeContext.Provider>
);
