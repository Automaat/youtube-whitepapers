import type { CSSProperties, ReactNode } from "react";
import { useCurrentFrame } from "remotion";
import { MONO, SANS, SERIF } from "./fonts";
import { enter, progress } from "./motion";
import { useTheme } from "./theme";
import { MARGIN } from "./tokens";

/** Absolutely positioned HTML box in frame pixels. */
export const Box = ({
  x,
  y,
  w,
  h,
  children,
  style,
}: {
  x: number;
  y: number;
  w?: number;
  h?: number;
  children: ReactNode;
  style?: CSSProperties;
}) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, height: h, ...style }}>{children}</div>
);

export const Serif = ({ size, children, color, style }: { size: number; children: ReactNode; color?: string; style?: CSSProperties }) => {
  const t = useTheme();
  return (
    <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: size, lineHeight: 1.08, color: color ?? t.heading, ...style }}>
      {children}
    </div>
  );
};

export const Text = ({
  size = 32,
  weight = 500,
  color,
  mono = false,
  children,
  style,
}: {
  size?: number;
  weight?: number;
  color?: string;
  mono?: boolean;
  children: ReactNode;
  style?: CSSProperties;
}) => {
  const t = useTheme();
  return (
    <div style={{ fontFamily: mono ? MONO : SANS, fontSize: size, fontWeight: weight, lineHeight: 1.3, color: color ?? t.ink, ...style }}>
      {children}
    </div>
  );
};

/** Inline technical term in mono. */
export const Term = ({ children, color }: { children: ReactNode; color?: string }) => (
  <span style={{ fontFamily: MONO, fontWeight: 700, color }}>{children}</span>
);

/** Optional scene title under the brand mark. Enters at `at`. */
export const SceneTitle = ({ children, at = 0 }: { children: ReactNode; at?: number }) => {
  const frame = useCurrentFrame();
  return (
    <Box x={MARGIN} y={124} style={enter(frame, at)}>
      <Serif size={60}>{children}</Serif>
    </Box>
  );
};

export const Card = ({
  x,
  y,
  w,
  h,
  children,
  glow = false,
  opacity = 1,
  style,
}: {
  x: number;
  y: number;
  w: number;
  h: number;
  children: ReactNode;
  glow?: boolean;
  opacity?: number;
  style?: CSSProperties;
}) => {
  const t = useTheme();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        background: t.surface,
        border: `2px solid ${glow ? t.heading : t.line}`,
        borderRadius: 22,
        boxShadow: glow ? `0 0 28px ${t.glow}` : undefined,
        opacity,
        padding: 32,
        boxSizing: "border-box",
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** Glossary card: icon area (SVG children, 316×230 viewBox) + term + short definition. */
export const TermCard = ({
  x,
  y,
  term,
  definition,
  icon,
  at = 0,
  w = 310,
  h = 470,
}: {
  x: number;
  y: number;
  term: string;
  definition: string;
  icon: ReactNode;
  at?: number;
  w?: number;
  h?: number;
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, ...enter(frame, at) }}>
      <Card x={0} y={0} w={w} h={h} style={{ padding: 0 }}>
        <svg width={w} height={230} viewBox="0 0 316 230" style={{ position: "absolute", left: 0, top: 20 }}>
          {icon}
        </svg>
        <div style={{ position: "absolute", left: 30, right: 24, top: 250 }}>
          <Text size={40} weight={700} mono>
            {term}
          </Text>
          <Text size={28} color={t.muted} style={{ marginTop: 14 }}>
            {definition}
          </Text>
        </div>
      </Card>
    </div>
  );
};

/** Row of a list: number badge, title, optional detail. `active` glows, `dim` fades to 30%. */
export const ListItem = ({
  index,
  title,
  detail,
  active = false,
  dim = false,
  at = 0,
  marker,
}: {
  index: number | string;
  title: ReactNode;
  detail?: ReactNode;
  active?: boolean;
  dim?: boolean;
  at?: number;
  marker?: ReactNode;
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const e = enter(frame, at);
  return (
    <div
      style={{
        display: "flex",
        gap: 28,
        alignItems: "flex-start",
        padding: "22px 28px",
        borderRadius: 18,
        background: active ? t.surface : "transparent",
        border: `2px solid ${active ? t.heading : "transparent"}`,
        boxShadow: active ? `0 0 24px ${t.glow}` : undefined,
        opacity: e.opacity * (dim ? 0.3 : 1),
        transform: e.transform,
      }}
    >
      <div style={{ minWidth: 56, height: 56, borderRadius: 28, background: active ? t.heading : t.inset, color: active ? t.brandInk : t.ink, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 700, fontSize: 28 }}>
        {marker ?? index}
      </div>
      <div>
        <Text size={38} weight={700}>
          {title}
        </Text>
        {detail ? (
          <Text size={28} color={t.muted} style={{ marginTop: 6 }}>
            {detail}
          </Text>
        ) : null}
      </div>
    </div>
  );
};

/** Short paper quote with source line. */
export const Quote = ({ x, y, w, text, source, at = 0 }: { x: number; y: number; w: number; text: string; source: string; at?: number }) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  return (
    <Box x={x} y={y} w={w} style={enter(frame, at)}>
      <div style={{ borderLeft: `6px solid ${t.heading}`, paddingLeft: 36 }}>
        <Serif size={48} color={t.ink} style={{ fontWeight: 500, lineHeight: 1.25 }}>
          „{text}”
        </Serif>
        <Text size={26} color={t.muted} mono style={{ marginTop: 22 }}>
          {source}
        </Text>
      </div>
    </Box>
  );
};

export type Bar = { label: string; value: number; color?: string; valueLabel?: string };

/** Horizontal bar chart. Bars grow from `at`, staggered. Title states the takeaway (pass it separately). */
export const BarChart = ({
  x,
  y,
  w,
  bars,
  max,
  at = 0,
  barHeight = 84,
  gap = 44,
  labelWidth = 260,
}: {
  x: number;
  y: number;
  w: number;
  bars: Bar[];
  max: number;
  at?: number;
  barHeight?: number;
  gap?: number;
  labelWidth?: number;
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const track = w - labelWidth - 180;
  return (
    <Box x={x} y={y} w={w}>
      {bars.map((b, i) => {
        const p = progress(frame, at + i * 12, 24);
        return (
          <div key={b.label} style={{ display: "flex", alignItems: "center", height: barHeight, marginBottom: gap }}>
            <Text size={34} weight={700} style={{ width: labelWidth }}>
              {b.label}
            </Text>
            <div style={{ position: "relative", width: track, height: barHeight, background: t.inset, borderRadius: 14 }}>
              <div style={{ width: (track * b.value * p) / max, height: "100%", background: b.color ?? t.muted, borderRadius: 14 }} />
            </div>
            <Text size={40} weight={700} mono style={{ marginLeft: 28, opacity: p }}>
              {b.valueLabel ?? b.value}
            </Text>
          </div>
        );
      })}
    </Box>
  );
};

/** Big number with caption (Fraunces). */
export const BigNumber = ({ x, y, value, caption, at = 0, color }: { x: number; y: number; value: string; caption: string; at?: number; color?: string }) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  return (
    <Box x={x} y={y} style={enter(frame, at)}>
      <Serif size={140} color={color ?? t.heading}>
        {value}
      </Serif>
      <Text size={32} color={t.muted} style={{ marginTop: 8 }}>
        {caption}
      </Text>
    </Box>
  );
};
