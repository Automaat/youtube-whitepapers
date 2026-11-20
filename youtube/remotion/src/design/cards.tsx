import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { Speaker } from "../timeline";
import { MONO, SANS, SERIF } from "./fonts";
import { enter, progress } from "./motion";
import { Diagram, Link, RoleNode } from "./svg";
import { useTheme } from "./theme";
import { MARGIN, ring } from "./tokens";
import { Box, Serif, Text } from "./ui";

const BARS = [10, 22, 14, 26, 12];

export const SpeakerChip = ({ speaker }: { speaker: Speaker }) => {
  const t = useTheme();
  const frame = useCurrentFrame();
  const skeptic = speaker === "skeptic";
  return (
    <div
      style={{
        position: "absolute",
        left: MARGIN,
        bottom: 44,
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "10px 22px 10px 16px",
        borderRadius: 999,
        background: skeptic ? t.brandTint : t.surface,
        color: skeptic ? t.brandInk : t.ink,
        border: `2px solid ${skeptic ? "transparent" : t.line}`,
        fontFamily: SANS,
        fontSize: 24,
        fontWeight: 600,
      }}
    >
      <span style={{ display: "flex", gap: 4, alignItems: "center", height: 26 }}>
        {BARS.map((h, i) => (
          <b
            key={i}
            style={{
              width: 5,
              borderRadius: 3,
              background: "currentColor",
              height: h * (0.6 + 0.4 * Math.abs(Math.sin(frame / 4 + i * 1.3))),
            }}
          />
        ))}
      </span>
      {skeptic ? "Sceptyk" : "Narrator"}
    </div>
  );
};

export const Chrome = ({
  number,
  title,
  chapters,
  chapterIndex,
  speaker,
}: {
  number: number;
  title: string;
  chapters: { id: string; title: string }[];
  chapterIndex: number;
  speaker: Speaker;
}) => {
  const t = useTheme();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: MARGIN, top: 44, fontFamily: SERIF, fontWeight: 600, fontSize: 30, color: t.heading }}>
        Głęboki Odczyt
        <span style={{ fontFamily: SANS, fontWeight: 500, fontSize: 24, color: t.muted, marginLeft: 10 }}>
          · #{number} {title}
        </span>
      </div>
      {chapterIndex >= 0 ? (
        <div style={{ position: "absolute", right: MARGIN, top: 50, display: "flex", alignItems: "center", gap: 18 }}>
          <span style={{ fontFamily: SANS, fontSize: 24, fontWeight: 600, color: t.muted }}>{chapters[chapterIndex]?.title}</span>
          <span style={{ display: "flex", gap: 8 }}>
            {chapters.map((c, i) => (
              <i
                key={c.id}
                style={{ width: 52, height: 8, borderRadius: 4, background: i < chapterIndex ? t.muted : i === chapterIndex ? t.heading : t.line }}
              />
            ))}
          </span>
        </div>
      ) : null}
      <SpeakerChip speaker={speaker} />
    </AbsoluteFill>
  );
};

/** Chapter card overlay, shown for ~2.5 s at the first scene of a chapter. */
export const ChapterCard = ({ chapters, index }: { chapters: { id: string; title: string }[]; index: number }) => {
  const t = useTheme();
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const inP = progress(frame, 0, 12);
  const outP = progress(frame, durationInFrames - 12, 12);
  return (
    <AbsoluteFill style={{ background: t.canvas, opacity: inP * (1 - outP) }}>
      <Box x={150} y={330} style={enter(frame, 4)}>
        <Text size={32} weight={700} color={t.muted} style={{ letterSpacing: "0.12em", textTransform: "uppercase" }}>
          Rozdział {index + 1}
        </Text>
        <Serif size={140} style={{ marginTop: 16, maxWidth: 950 }}>
          {chapters[index]?.title}
        </Serif>
      </Box>
      <Box x={1180} y={290} w={600}>
        {chapters.map((c, i) => (
          <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 24, padding: "16px 0", borderBottom: `2px solid ${t.line}`, opacity: i === index ? 1 : 0.45 }}>
            <span style={{ fontFamily: MONO, fontSize: 28, color: i === index ? t.heading : t.muted, width: 40 }}>{i + 1}</span>
            <Text size={34} weight={i === index ? 700 : 500}>
              {c.title}
            </Text>
          </div>
        ))}
      </Box>
    </AbsoluteFill>
  );
};

/** Episode title card; also used as the thumbnail when no image exists. */
export const TitleCard = ({
  number,
  title,
  subtitle,
  authors,
  at = 0,
}: {
  number: number;
  title: string;
  subtitle: string;
  authors: string;
  at?: number;
}) => {
  const t = useTheme();
  const frame = useCurrentFrame();
  const pts = ring(1480, 560, 200, 5);
  return (
    <AbsoluteFill style={{ background: t.canvas }}>
      <Box x={150} y={300} w={950} style={enter(frame, at)}>
        <Text size={28} weight={700} color={t.muted} style={{ letterSpacing: "0.12em", textTransform: "uppercase" }}>
          Głęboki Odczyt · odcinek {number}
        </Text>
        <Serif size={title.length > 8 ? 160 : 250} style={{ lineHeight: 1, margin: "18px 0 26px" }}>
          {title}
        </Serif>
        <Text size={46} weight={500} style={{ lineHeight: 1.25 }}>
          {subtitle}
        </Text>
        <Text size={28} color={t.muted} style={{ marginTop: 26 }}>
          {authors}
        </Text>
      </Box>
      <Diagram>
        {pts.flatMap((p, i) => pts.slice(i + 1).map((q, j) => <Link key={`${i}-${j}`} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} opacity={progress(frame, at + 10, 20)} />))}
        {pts.map((p, i) => (
          <g key={i} opacity={progress(frame, at + 6 + i * 5, 12)}>
            <RoleNode x={p[0]} y={p[1]} label={`S${i + 1}`} role={i === 0 && frame >= at + 40 ? "leader" : "follower"} r={48} />
          </g>
        ))}
      </Diagram>
    </AbsoluteFill>
  );
};

/** 5 s silent outro: "Polub i subskrybuj" in the episode style, no mascot. */
export const OutroCard = () => {
  const t = useTheme();
  const frame = useCurrentFrame();
  const pulse = interpolate(frame % 45, [0, 45], [0, 1]);
  const pts = ring(960, 430, 150, 5);
  return (
    <AbsoluteFill style={{ background: t.canvas }}>
      <Diagram>
        {pts.flatMap((p, i) => pts.slice(i + 1).map((q, j) => <Link key={`${i}-${j}`} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} opacity={progress(frame, 6, 18)} />))}
        <circle cx={960} cy={430} r={150 + pulse * 160} fill="none" stroke={t.heading} strokeWidth={4} opacity={(1 - pulse) * 0.5} />
        {pts.map((p, i) => (
          <g key={i} opacity={progress(frame, i * 4, 12)}>
            <RoleNode x={p[0]} y={p[1]} label="" role={i === 0 ? "leader" : "follower"} r={34} />
          </g>
        ))}
        {/* bell */}
        <g transform="translate(560 430)" opacity={progress(frame, 14, 14)}>
          <circle r={86} fill={t.surface} stroke={t.line} strokeWidth={3} />
          <path d="M-34 22 C-34 -6 -28 -40 0 -44 C28 -40 34 -6 34 22 L44 34 L-44 34 Z" fill={t.heading} transform={`rotate(${Math.sin(frame / 3) * 10 * (1 - progress(frame, 40, 30))})`} />
          <circle cx={0} cy={46} r={10} fill={t.heading} />
        </g>
        {/* thumb */}
        <g transform="translate(1360 430)" opacity={progress(frame, 20, 14)}>
          <circle r={86} fill={t.surface} stroke={t.line} strokeWidth={3} />
          <path d="M-40 -6 H-22 V42 H-40 Z M-14 -6 L4 -42 C16 -44 20 -32 16 -20 L12 -8 H38 C48 -8 52 0 50 8 L42 36 C40 42 34 44 28 44 H-14 Z" fill={t.heading} />
        </g>
      </Diagram>
      <Box x={0} y={700} w={1920} style={{ textAlign: "center", ...enter(frame, 10, 18) }}>
        <Serif size={120}>Polub i subskrybuj</Serif>
        <Text size={36} color={t.muted} style={{ marginTop: 20 }}>
          Głęboki Odczyt · do zobaczenia w kolejnym odcinku
        </Text>
      </Box>
    </AbsoluteFill>
  );
};
