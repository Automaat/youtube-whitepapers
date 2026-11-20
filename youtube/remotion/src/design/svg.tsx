import type { ReactNode } from "react";
import { MONO, SANS } from "./fonts";
import { along, alongCurve } from "./motion";
import { useTheme } from "./theme";
import { HEIGHT, WIDTH, type Theme } from "./tokens";

export type Role = "leader" | "candidate" | "c3" | "follower" | "crashed";

/** Full-frame SVG layer in 1920×1080 coordinates. */
export const Diagram = ({ children }: { children: ReactNode }) => (
  <svg
    viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
    width={WIDTH}
    height={HEIGHT}
    style={{ position: "absolute", inset: 0, overflow: "visible" }}
  >
    {children}
  </svg>
);

/** Group with opacity and optional pink glow (the "active element" signal). */
export const G = ({
  children,
  opacity = 1,
  glow = false,
  transform,
}: {
  children: ReactNode;
  opacity?: number;
  glow?: boolean;
  transform?: string;
}) => {
  const t = useTheme();
  return (
    <g
      opacity={opacity}
      transform={transform}
      style={glow ? { filter: `drop-shadow(0 0 16px ${t.glow}) drop-shadow(0 0 4px ${t.glow})` } : undefined}
    >
      {children}
    </g>
  );
};

export const roleStyle = (t: Theme, role: Role) =>
  ({
    leader: { fill: t.leader, stroke: "none", text: t.onRole, dash: undefined },
    candidate: { fill: t.candidate, stroke: "none", text: t.onRole, dash: undefined },
    c3: { fill: t.c3, stroke: "none", text: t.onRole, dash: undefined },
    follower: { fill: t.surface, stroke: t.muted, text: t.ink, dash: undefined },
    crashed: { fill: t.inset, stroke: t.line, text: t.muted, dash: "8 8" },
  })[role];

/** SVG text label. Sizes in px at 1080p; keep ≥ 22. */
export const Label = ({
  x,
  y,
  children,
  size = 28,
  weight = 600,
  anchor = "middle",
  mono = false,
  color,
  opacity = 1,
}: {
  x: number;
  y: number;
  children: ReactNode;
  size?: number;
  weight?: number;
  anchor?: "start" | "middle" | "end";
  mono?: boolean;
  color?: string;
  opacity?: number;
}) => {
  const t = useTheme();
  return (
    <text
      x={x}
      y={y}
      textAnchor={anchor}
      opacity={opacity}
      style={{ fill: color ?? t.ink, fontFamily: mono ? MONO : SANS, fontSize: size, fontWeight: weight }}
    >
      {children}
    </text>
  );
};

export const Cross = ({ x, y, s = 22 }: { x: number; y: number; s?: number }) => {
  const t = useTheme();
  const d = s * 0.4;
  return (
    <g>
      <circle cx={x} cy={y} r={s} fill={t.canvas} stroke={t.danger} strokeWidth={4} />
      <path
        d={`M${x - d} ${y - d} L${x + d} ${y + d} M${x + d} ${y - d} L${x - d} ${y + d}`}
        stroke={t.danger}
        strokeWidth={5}
        strokeLinecap="round"
      />
    </g>
  );
};

export const Check = ({ x, y, s = 20 }: { x: number; y: number; s?: number }) => {
  const t = useTheme();
  return (
    <g>
      <circle cx={x} cy={y} r={s} fill={t.success} />
      <path
        d={`M${x - s * 0.45} ${y} L${x - s * 0.1} ${y + s * 0.35} L${x + s * 0.5} ${y - s * 0.35}`}
        fill="none"
        stroke={t.canvas}
        strokeWidth={5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </g>
  );
};

/** Server / actor node. `crashed` draws a dashed outline and a ✕ badge. */
export const RoleNode = ({
  x,
  y,
  label,
  role,
  r = 50,
  sub,
  fontSize,
}: {
  x: number;
  y: number;
  label: string;
  role: Role;
  r?: number;
  sub?: string;
  fontSize?: number;
}) => {
  const t = useTheme();
  const s = roleStyle(t, role);
  const fs = fontSize ?? Math.max(22, r * 0.56);
  return (
    <g>
      <circle cx={x} cy={y} r={r} fill={s.fill} stroke={s.stroke} strokeWidth={4} strokeDasharray={s.dash} />
      <Label x={x} y={y + fs * 0.36} size={fs} weight={700} mono color={s.text}>
        {label}
      </Label>
      {sub ? (
        <Label x={x} y={y + r + 40} size={26} color={t.muted}>
          {sub}
        </Label>
      ) : null}
      {role === "crashed" ? <Cross x={x + r * 0.72} y={y - r * 0.72} s={20} /> : null}
    </g>
  );
};

/** Rounded pill for a state in a state machine. */
export const StatePill = ({
  x,
  y,
  label,
  role,
  w = 320,
  h = 120,
}: {
  x: number;
  y: number;
  label: string;
  role: Role;
  w?: number;
  h?: number;
}) => {
  const t = useTheme();
  const s = roleStyle(t, role);
  return (
    <g>
      <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={h / 2} fill={s.fill} stroke={s.stroke} strokeWidth={4} strokeDasharray={s.dash} />
      <Label x={x} y={y + 14} size={40} weight={700} mono color={s.text}>
        {label}
      </Label>
    </g>
  );
};

const head = (x1: number, y1: number, x2: number, y2: number, size: number) => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  const p = (o: number) => [x2 - size * Math.cos(a + o * 0.45), y2 - size * Math.sin(a + o * 0.45)];
  const [ax, ay] = p(1);
  const [bx, by] = p(-1);
  return `${x2},${y2} ${ax},${ay} ${bx},${by}`;
};

/** Straight arrow. `progress` < 1 draws it partially (head appears at 1). */
export const Arrow = ({
  x1,
  y1,
  x2,
  y2,
  color,
  width = 4,
  dashed = false,
  progress = 1,
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  color?: string;
  width?: number;
  dashed?: boolean;
  progress?: number;
}) => {
  const t = useTheme();
  const c = color ?? t.muted;
  if (progress <= 0) return null;
  const a = Math.atan2(y2 - y1, x2 - x1);
  const [ex, ey] = along(x1, y1, x2 - 10 * Math.cos(a), y2 - 10 * Math.sin(a), progress);
  return (
    <g>
      <line x1={x1} y1={y1} x2={ex} y2={ey} stroke={c} strokeWidth={width} strokeLinecap="round" strokeDasharray={dashed ? "10 10" : undefined} />
      {progress >= 1 ? <polygon points={head(x1, y1, x2, y2, 18)} fill={c} /> : null}
    </g>
  );
};

/** Quadratic curved arrow through control point (cx, cy). */
export const CurvedArrow = ({
  x1,
  y1,
  cx,
  cy,
  x2,
  y2,
  color,
  width = 4,
  progress = 1,
}: {
  x1: number;
  y1: number;
  cx: number;
  cy: number;
  x2: number;
  y2: number;
  color?: string;
  width?: number;
  progress?: number;
}) => {
  const t = useTheme();
  const c = color ?? t.muted;
  if (progress <= 0) return null;
  const steps = 40;
  const pts = Array.from({ length: Math.max(2, Math.round(steps * progress)) + 1 }, (_, i) =>
    alongCurve(x1, y1, cx, cy, x2, y2, (i / Math.max(2, Math.round(steps * progress))) * progress),
  );
  const [px, py] = alongCurve(x1, y1, cx, cy, x2, y2, 0.97);
  return (
    <g>
      <polyline points={pts.map((p) => p.join(",")).join(" ")} fill="none" stroke={c} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" />
      {progress >= 1 ? <polygon points={head(px, py, x2, y2, 22)} fill={c} /> : null}
    </g>
  );
};

/** Plain connection between two nodes. */
export const Link = ({ x1, y1, x2, y2, dashed = false, opacity = 1 }: { x1: number; y1: number; x2: number; y2: number; dashed?: boolean; opacity?: number }) => {
  const t = useTheme();
  return <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={t.line} strokeWidth={3} strokeDasharray={dashed ? "8 10" : undefined} opacity={opacity} />;
};

/** A message in flight: a dot moving from (x1,y1) to (x2,y2); hidden outside 0 < t < 1. Optional curve via (cx, cy). */
export const Message = ({
  x1,
  y1,
  x2,
  y2,
  t: tt,
  color,
  r = 12,
  cx,
  cy,
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  t: number;
  color?: string;
  r?: number;
  cx?: number;
  cy?: number;
}) => {
  const theme = useTheme();
  if (tt <= 0 || tt >= 1) return null;
  const [x, y] = cx !== undefined && cy !== undefined ? alongCurve(x1, y1, cx, cy, x2, y2, tt) : along(x1, y1, x2, y2, tt);
  return <circle cx={x} cy={y} r={r} fill={color ?? theme.heading} />;
};

/** Small pill with text, e.g. "term 2" or "?". */
export const Badge = ({
  x,
  y,
  text,
  color,
  textColor,
  stroke,
  mono = true,
  size = 26,
}: {
  x: number;
  y: number;
  text: string;
  color?: string;
  textColor?: string;
  stroke?: string;
  mono?: boolean;
  size?: number;
}) => {
  const t = useTheme();
  const w = Math.max(size * 1.7, text.length * size * (mono ? 0.62 : 0.58) + size * 1.2);
  const h = size * 1.75;
  return (
    <g>
      <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={h / 2} fill={color ?? t.inset} stroke={stroke ?? t.line} strokeWidth={2} />
      <Label x={x} y={y + size * 0.36} size={size} weight={700} mono={mono} color={textColor ?? t.ink}>
        {text}
      </Label>
    </g>
  );
};

/** Swimlane: label node on the left and a horizontal line. */
export const Lane = ({
  y,
  label,
  role = "follower",
  x1 = 170,
  x2 = 1800,
}: {
  y: number;
  label: string;
  role?: Role;
  x1?: number;
  x2?: number;
}) => {
  const t = useTheme();
  return (
    <g>
      <line x1={x1 + 60} y1={y} x2={x2} y2={y} stroke={t.line} strokeWidth={3} strokeDasharray={role === "crashed" ? "8 10" : undefined} />
      <RoleNode x={x1} y={y} label={label} role={role} r={34} fontSize={24} />
    </g>
  );
};

/** Timer bar growing from x over width w. */
export const TimerBar = ({
  x,
  y,
  w,
  progress,
  color,
  h = 18,
}: {
  x: number;
  y: number;
  w: number;
  progress: number;
  color?: string;
  h?: number;
}) => {
  const t = useTheme();
  return (
    <g>
      <rect x={x} y={y - h / 2} width={w} height={h} rx={h / 2} fill={t.inset} stroke={t.line} strokeWidth={2} />
      <rect x={x} y={y - h / 2} width={Math.max(0, w * progress)} height={h} rx={h / 2} fill={color ?? t.candidate} opacity={0.75} />
    </g>
  );
};

export type CellState = "committed" | "pending" | "empty" | "conflict";

/** Log entry cell: term number on top, command below. */
export const LogCell = ({
  x,
  y,
  w = 110,
  h = 96,
  term,
  cmd,
  state = "pending",
  termColor,
}: {
  x: number;
  y: number;
  w?: number;
  h?: number;
  term?: number | string;
  cmd?: string;
  state?: CellState;
  termColor?: string;
}) => {
  const t = useTheme();
  const fill = state === "committed" ? t.successSoft : state === "empty" ? "none" : t.surface;
  const stroke = state === "committed" ? t.success : state === "conflict" ? t.danger : state === "empty" ? t.line : t.muted;
  const dash = state === "pending" || state === "empty" ? "9 7" : undefined;
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={12} fill={fill} stroke={stroke} strokeWidth={3} strokeDasharray={dash} />
      {term !== undefined ? (
        <Label x={x + 16} y={y + 40} size={32} weight={700} mono anchor="start" color={termColor ?? t.ink}>
          {String(term)}
        </Label>
      ) : null}
      {cmd ? (
        <Label x={x + 16} y={y + h - 16} size={22} weight={500} mono anchor="start" color={t.muted}>
          {cmd}
        </Label>
      ) : null}
      {state === "conflict" ? <Cross x={x + w - 6} y={y + 6} s={16} /> : null}
    </g>
  );
};
