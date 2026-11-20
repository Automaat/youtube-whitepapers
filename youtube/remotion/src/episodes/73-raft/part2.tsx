import type { FC, ReactNode } from "react";
import {
  Arrow,
  Badge,
  Check,
  Cross,
  CurvedArrow,
  DIM,
  Diagram,
  G,
  Label,
  Lane,
  Message,
  RoleNode,
  StatePill,
  TimerBar,
  alongCurve,
  focusOpacity,
  linear,
  progress,
  useScene,
  useTheme,
  type Role,
} from "../../design";
import { LANE_X1, LANE_X2, LANE_Y, NODE_R, RIBBON_Y, RING, RING_CENTER, SERVERS, type Server } from "./layout";

const opacityAt = (f: number, at: number, until = Infinity) => progress(f, at, 12) * focusOpacity(f, at, until);
const dimAfter = (f: number, at: number) => 1 - (1 - DIM) * progress(f, at, 10);
const riseAt =(f: number, at: number) => `translate(0 ${(1 - progress(f, at, 15)) * 24})`;

const Phase = ({ f, at, until = Infinity, glow = true, children }: { f: number; at: number; until?: number; glow?: boolean; children: ReactNode }) => (
  <G opacity={opacityAt(f, at, until)} glow={glow && f >= at && f < until} transform={riseAt(f, at)}>
    {children}
  </G>
);

const shorten = (a: [number, number], b: [number, number], d1: number, d2: number, off = 0) => {
  const dx = b[0] - a[0];
  const dy = b[1] - a[1];
  const len = Math.hypot(dx, dy);
  const ux = dx / len;
  const uy = dy / len;
  const ox = -uy * off;
  const oy = ux * off;
  return { x1: a[0] + ux * d1 + ox, y1: a[1] + uy * d1 + oy, x2: b[0] - ux * d2 + ox, y2: b[1] - uy * d2 + oy };
};

// ---------------------------------------------------------------- key_insight

const KeyInsight: FC = () => {
  const { frame: f, cue } = useScene();
  const t = useTheme();
  const cLeader = cue("strong_leader");
  const cFlow = cue("one_way_flow");
  const cThree = cue("decompose_three");
  const cHoles = cue("state_space");
  const isLeader = f >= cLeader;
  const ringOp = dimAfter(f, cThree);
  const followers = SERVERS.filter((s) => s !== "S1");
  const back = shorten(RING.S3, RING.S1, NODE_R + 10, NODE_R + 10, -24);
  const chips = ["Leader election", "Log replication", "Safety"];
  // Badge width formula from the design system (mono, size 28), packed with a fixed gap and centered under the ring.
  const chipW = chips.map((c) => Math.max(28 * 1.7, c.length * 28 * 0.62 + 28 * 1.2));
  const chipGap = 32;
  const chipTotal = chipW.reduce((a, b) => a + b, 0) + chipGap * (chips.length - 1);
  const chipX = chipW.map((w, i) => RING_CENTER[0] - chipTotal / 2 + chipW.slice(0, i).reduce((a, b) => a + b, 0) + chipGap * i + w / 2);
  return (
    <Diagram>
      <G opacity={ringOp}>
        <G opacity={progress(f, cFlow, 12)} glow={f >= cFlow && f < cThree}>
          {followers.map((s, i) => {
            const a = shorten(RING.S1, RING[s], NODE_R + 10, NODE_R + 10, s === "S3" ? -22 : 0);
            return (
              <g key={s}>
                <Arrow {...a} color={t.leader} width={5} progress={progress(f, cFlow + i * 3, 18)} />
                {[0, 40].map((d) => (
                  <Message key={d} x1={a.x1} y1={a.y1} x2={a.x2} y2={a.y2} t={linear(f, cFlow + 18 + d + i * 3, 24)} color={t.leader} />
                ))}
              </g>
            );
          })}
          <g opacity={progress(f, cFlow + 70, 12)}>
            <Arrow {...back} color={t.danger} width={4} dashed />
            <Cross x={(back.x1 + back.x2) / 2} y={(back.y1 + back.y2) / 2} s={22} />
          </g>
        </G>
        {SERVERS.map((s) => (
          <G key={s} glow={s === "S1" && isLeader && f < cFlow}>
            <RoleNode x={RING[s][0]} y={RING[s][1]} label={s} role={s === "S1" && isLeader ? "leader" : "follower"} r={NODE_R} />
          </G>
        ))}
        <g opacity={progress(f, cLeader, 12)}>
          <Label x={RING.S1[0]} y={RING.S1[1] - NODE_R - 22} size={30} weight={700} mono>
            Leader
          </Label>
        </g>
      </G>
      {chips.map((c, i) => (
        <G key={c} opacity={progress(f, cThree + i * 12, 12) * dimAfter(f, cHoles)} glow={i === 0 && f >= cThree && f < cHoles} transform={riseAt(f, cThree + i * 12)}>
          <Badge x={chipX[i]} y={918} text={c} size={28} stroke={i === 0 && f < cHoles ? t.heading : undefined} />
        </G>
      ))}
      <Phase f={f} at={cHoles}>
        <Label x={1537} y={515} size={30} weight={700}>
          log bez dziur
        </Label>
        {["x←3", "y←1", "x←2"].map((cmd, i) => (
          <g key={cmd}>
            <rect x={1360 + i * 122} y={545} width={110} height={88} rx={12} fill={t.surface} stroke={t.muted} strokeWidth={3} />
            <Label x={1376 + i * 122} y={585} size={32} weight={700} mono anchor="start">
              1
            </Label>
            <Label x={1376 + i * 122} y={617} size={22} weight={500} mono anchor="start" color={t.muted}>
              {cmd}
            </Label>
          </g>
        ))}
      </Phase>
    </Diagram>
  );
};

// ---------------------------------------------------------------- server_states

type Arc = [number, number, number, number, number, number];
const ARC: Record<"fc" | "loop" | "cl" | "cf" | "lf", Arc> = {
  fc: [500, 500, 690, 330, 880, 500],
  loop: [910, 500, 960, 230, 1010, 500],
  cl: [1040, 500, 1230, 320, 1420, 500],
  cf: [900, 620, 700, 780, 520, 620],
  lf: [1480, 620, 950, 1010, 380, 620],
};
const PILL_X = { F: 420, C: 960, L: 1500 };
const PILL_Y = 560;

const ServerStates: FC = () => {
  const { frame: f, cue } = useScene();
  const t = useTheme();
  const c = {
    start: cue("start_follower"),
    fc: cue("timeout_to_candidate"),
    cl: cue("majority_to_leader"),
    loop: cue("retry_loop"),
    down: cue("step_down"),
  };
  const phase = f < c.start ? -1 : f < c.fc ? 0 : f < c.cl ? 1 : f < c.loop ? 2 : f < c.down ? 3 : 4;
  const involved: Record<number, string[]> = { [-1]: ["F", "C", "L"], 0: ["F"], 1: ["F", "C"], 2: ["C", "L"], 3: ["C"], 4: ["F", "C", "L"] };
  const pillOp = (k: string) => (involved[phase].includes(k) ? 1 : DIM);

  const arc = (
    k: keyof typeof ARC,
    at: number,
    until: number,
    label: ReactNode,
    lx: number,
    ly: number,
    extra?: keyof typeof ARC,
    extraLabel?: [number, number],
  ) => {
    const [x1, y1, cx, cy, x2, y2] = ARC[k];
    const active = f >= at && f < until;
    const col = active ? t.heading : t.muted;
    return (
      <G opacity={opacityAt(f, at, until)} glow={active}>
        <CurvedArrow x1={x1} y1={y1} cx={cx} cy={cy} x2={x2} y2={y2} color={col} width={active ? 6 : 4} progress={progress(f, at, 24)} />
        {extra ? (
          <CurvedArrow x1={ARC[extra][0]} y1={ARC[extra][1]} cx={ARC[extra][2]} cy={ARC[extra][3]} x2={ARC[extra][4]} y2={ARC[extra][5]} color={col} width={active ? 6 : 4} progress={progress(f, at + 6, 24)} />
        ) : null}
        <Label x={lx} y={ly} size={30} weight={600}>
          {label}
        </Label>
        {extraLabel ? (
          <Label x={extraLabel[0]} y={extraLabel[1]} size={30} weight={600}>
            {label}
          </Label>
        ) : null}
      </G>
    );
  };

  const travel = (k: keyof typeof ARC, at: number): [number, number] => {
    const [x1, y1, cx, cy, x2, y2] = ARC[k];
    return alongCurve(x1, y1, cx, cy, x2, y2, progress(f, at + 4, 30));
  };
  const token: [number, number] | null =
    phase < 0
      ? null
      : phase === 0
        ? [120 + (258 - 120) * progress(f, c.start, 20), PILL_Y]
        : phase === 1
          ? travel("fc", c.fc)
          : phase === 2
            ? travel("cl", c.cl)
            : phase === 3
              ? travel("loop", c.loop)
              : travel("lf", c.down);

  return (
    <Diagram>
      <G opacity={opacityAt(f, c.start, c.fc)} glow={phase === 0}>
        <Arrow x1={120} y1={PILL_Y} x2={256} y2={PILL_Y} color={phase === 0 ? t.heading : t.muted} width={5} progress={progress(f, c.start, 15)} />
        <Label x={178} y={PILL_Y - 34} size={26} color={t.muted}>
          start
        </Label>
      </G>
      {arc("fc", c.fc, c.cl, "timeout", 690, 390)}
      {arc("cl", c.cl, c.loop, "większość głosów", 1230, 372)}
      {arc("loop", c.loop, c.down, "timeout, nowe wybory", 935, 288)}
      {arc("cf", c.down, Infinity, "wyższy term", 950, 876, "lf", [715, 654])}
      {(
        [
          ["F", "Follower", "follower"],
          ["C", "Candidate", "candidate"],
          ["L", "Leader", "leader"],
        ] as const
      ).map(([k, label, role], i) => (
        <G key={k} opacity={pillOp(k) * progress(f, i * 8, 15)} glow={phase === 0 ? k === "F" : false} transform={riseAt(f, i * 8)}>
          <StatePill x={PILL_X[k]} y={PILL_Y} label={label} role={role as Role} />
        </G>
      ))}
      {token ? (
        <G glow>
          <circle cx={token[0]} cy={token[1]} r={14} fill={t.heading} />
        </G>
      ) : null}
    </Diagram>
  );
};

// ---------------------------------------------------------------- shared swimlane pieces

const RibbonSeg = ({ x1, x2, label }: { x1: number; x2: number; label?: string }) => {
  const t = useTheme();
  return (
    <g>
      <rect x={x1} y={RIBBON_Y - 22} width={x2 - x1} height={44} rx={12} fill="none" stroke={t.c3} strokeWidth={3} />
      {label ? (
        <Label x={x1 + 4} y={RIBBON_Y - 36} size={26} mono anchor="start">
          {label}
        </Label>
      ) : null}
    </g>
  );
};

const RibbonBlock = ({ x1, x2, kind, p = 1 }: { x1: number; x2: number; kind: "election" | "leader"; p?: number }) => {
  const t = useTheme();
  if (p <= 0) return null;
  return <rect x={x1 + 6} y={RIBBON_Y - 15} width={Math.max(0, (x2 - x1 - 12) * p)} height={30} rx={8} fill={kind === "election" ? t.candidate : t.leader} />;
};

const Lanes = ({ roles }: { roles: Partial<Record<Server, Role>> }) => (
  <g>
    {SERVERS.map((s) => (
      <Lane key={s} y={LANE_Y[s]} label={s} role={roles[s] ?? "follower"} x1={LANE_X1} x2={LANE_X2} />
    ))}
  </g>
);

const Dot = ({ x, y, role }: { x: number; y: number; role: "candidate" | "leader" }) => {
  const t = useTheme();
  return <circle cx={x} cy={y} r={20} fill={role === "candidate" ? t.candidate : t.leader} />;
};

/** Arrow drawn over `dur` frames with a dot riding its tip. */
const Shot = ({ f, at, x1, y1, x2, y2, color, dashed = false, dur = 20 }: { f: number; at: number; x1: number; y1: number; x2: number; y2: number; color: string; dashed?: boolean; dur?: number }) => {
  const p = linear(f, at, dur);
  return (
    <g>
      <Arrow x1={x1} y1={y1} x2={x2} y2={y2} color={color} width={4} dashed={dashed} progress={p} />
      <Message x1={x1} y1={y1} x2={x2} y2={y2} t={p} color={color} r={10} />
    </g>
  );
};

/** One RPC sent in parallel: a separate arrow from the sender's lane to each target lane, all leaving at the same moment. */
const Fan = ({
  f,
  at,
  x,
  from,
  to,
  dx = 50,
  color,
  dashed = [],
  dur = 20,
}: {
  f: number;
  at: number;
  x: number;
  from: number;
  to: number[];
  dx?: number;
  color: string;
  dashed?: number[];
  dur?: number;
}) => {
  const p = linear(f, at, dur);
  if (p <= 0) return null;
  return (
    <g>
      {to.map((y) => {
        const s = Math.sign(y - from);
        const a = { x1: x, y1: from + s * 22, x2: x + dx, y2: y - s * 14 };
        return (
          <g key={y}>
            <Arrow {...a} color={color} width={4} dashed={dashed.includes(y)} progress={p} />
            <Message {...a} t={p} color={color} r={10} />
          </g>
        );
      })}
    </g>
  );
};

// ---------------------------------------------------------------- terms

const TermChip = ({ y, term, active }: { y: number; term: number; active: boolean }) => {
  const t = useTheme();
  return <Badge x={330} y={y} text={`term ${term}`} size={24} color={t.canvas} stroke={active ? t.heading : t.c3} />;
};

const Terms: FC = () => {
  const { frame: f, cue } = useScene();
  const t = useTheme();
  const cRibbon = cue("term_ribbon");
  const cSplit = cue("split_term");
  const cCounters = cue("term_counters");
  const cCatch = cue("catch_up");
  const cStale = cue("stale_reject");
  const segs: { x1: number; x2: number; label: string; leader: boolean }[] = [
    { x1: 420, x2: 800, label: "term 1", leader: true },
    { x1: 810, x2: 1190, label: "term 2", leader: true },
    { x1: 1200, x2: 1400, label: "term 3", leader: false },
    { x1: 1410, x2: 1780, label: "term 4", leader: true },
  ];
  const ribbonOp = f < cSplit ? opacityAt(f, cRibbon) : dimAfter(f, cCounters);
  const lanesOp = f < cRibbon ? 1 : f < cCounters ? DIM + (1 - DIM) * (1 - progress(f, cRibbon, 10)) : DIM + (1 - DIM) * progress(f, cCounters, 10);
  const catchArrive = cCatch + 34;
  const staleArrive = cStale + 30;
  const s1Stale = f < staleArrive + 10;
  const terms: Record<Server, number> = { S1: s1Stale ? 1 : 2, S2: 2, S3: 2, S4: 2, S5: f >= catchArrive ? 2 : 1 };
  const catchMsg = { x1: 900, y1: LANE_Y.S2 + 10, x2: 980, y2: LANE_Y.S5 - 12 };
  const staleMsg = { x1: 1040, y1: LANE_Y.S1 + 12, x2: 1080, y2: LANE_Y.S2 - 26 };
  const pc = linear(f, cCatch, 34);
  const [bx, by] = [catchMsg.x1 + (catchMsg.x2 - catchMsg.x1) * pc, catchMsg.y1 + (catchMsg.y2 - catchMsg.y1) * pc];
  return (
    <Diagram>
      <G opacity={lanesOp}>
        <Lanes roles={{ S1: s1Stale ? "leader" : "follower" }} />
      </G>
      <G opacity={ribbonOp} glow={f >= cRibbon && f < cSplit}>
        {segs.map((s, i) => {
          const at = cRibbon + i * 12;
          const segOp = f >= cSplit && f < cCounters && i !== 2 ? DIM : 1;
          return (
            <G key={s.label} opacity={progress(f, at, 12) * segOp} glow={f >= cSplit && f < cCounters && i === 2}>
              <RibbonSeg x1={s.x1} x2={s.x2} label={s.label} />
              <RibbonBlock x1={s.x1} x2={s.x1 + 90} kind="election" p={progress(f, at + 4, 12)} />
              {s.leader ? <RibbonBlock x1={s.x1 + 84} x2={s.x2} kind="leader" p={progress(f, at + 12, 18)} /> : null}
              {!s.leader ? (
                <g opacity={progress(f, cSplit, 12)}>
                  <Cross x={s.x1 + 140} y={RIBBON_Y} s={20} />
                  <Label x={s.x1 + 100} y={RIBBON_Y + 62} size={26} weight={700}>
                    brak leadera
                  </Label>
                </g>
              ) : null}
            </G>
          );
        })}
      </G>
      {SERVERS.map((s, i) => {
        const at = cCounters + i * 5;
        const activeS5 = s === "S5" && f >= cCatch && f < cStale;
        const activeS1 = s === "S1" && f >= cStale;
        const op = f < cCatch ? opacityAt(f, at) : activeS5 || activeS1 ? 1 : DIM + (1 - DIM) * (1 - progress(f, cCatch, 10));
        return (
          <g key={s}>
            <rect x={268} y={LANE_Y[s] - 23} width={124} height={46} rx={23} fill={t.canvas} opacity={progress(f, at, 12)} />
            <G opacity={op} glow={(f >= cCounters && f < cCatch) || activeS5 || activeS1} transform={riseAt(f, at)}>
              <TermChip y={LANE_Y[s]} term={terms[s]} active={activeS5 || activeS1} />
            </G>
          </g>
        );
      })}
      <G opacity={opacityAt(f, cCatch, cStale)} glow={f >= cCatch && f < cStale}>
        <Arrow {...catchMsg} color={t.c3} width={4} progress={pc} />
        {pc > 0 && pc < 1 ? <Badge x={bx + 70} y={by} text="term 2" size={22} stroke={t.c3} /> : null}
      </G>
      <G opacity={opacityAt(f, cStale)} glow={f >= cStale}>
        <Shot f={f} at={cStale} {...staleMsg} color={t.leader} dur={30} />
        <g opacity={progress(f, cStale, 10)}>
          <Badge x={(staleMsg.x1 + staleMsg.x2) / 2 + 90} y={(LANE_Y.S1 + LANE_Y.S2) / 2} text="term 1" size={22} stroke={t.leader} />
        </g>
        <g opacity={progress(f, staleArrive, 10)}>
          <Cross x={staleMsg.x2 + 4} y={LANE_Y.S2} s={24} />
        </g>
      </G>
    </Diagram>
  );
};

// ---------------------------------------------------------------- election

const HB_X = [340, 500, 660];
const HB_DX = 60;
const FOLLOWERS: Server[] = ["S2", "S3", "S4", "S5"];
const FOLLOWER_LANES = FOLLOWERS.map((s) => LANE_Y[s]);
const hbArrive = (x: number) => x + HB_DX;
// Each heartbeat restarts every follower's timer at the x where it lands.
const timerStart = (X: number) => {
  const last = HB_X.filter((x) => X >= hbArrive(x)).pop();
  return last !== undefined ? hbArrive(last) : 300;
};

type ElectionCues = { heartbeats: number; leader_crash: number; s3_timeout: number; request_votes: number; majority_votes: number; new_leader: number };

const ElectionView = ({ f, c }: { f: number; c: ElectionCues }) => {
  const t = useTheme();
  const T: Record<Server, number> = { S1: 0, S2: 260, S3: 200, S4: 300, S5: 280 };
  const X =
    f < c.leader_crash
      ? 300 + 520 * linear(f, c.heartbeats, c.leader_crash - c.heartbeats)
      : 820 + 100 * linear(f, c.leader_crash, Math.min(45, c.s3_timeout - c.leader_crash));
  const hbFrame = (x: number) => c.heartbeats + ((x - 300) / 520) * (c.leader_crash - c.heartbeats);
  const crashed = f >= c.leader_crash;
  const s3Role: Role = f >= c.new_leader ? "leader" : f >= c.s3_timeout ? "candidate" : "follower";
  const y3 = LANE_Y.S3;
  return (
    <g>
      <Lanes roles={{ S1: crashed ? "crashed" : "leader", S3: s3Role }} />
      <G opacity={f >= c.s3_timeout ? DIM : 1}>
        <RibbonSeg x1={300} x2={912} label="term 1" />
        <RibbonBlock x1={300} x2={820} kind="leader" p={Math.min(1, (X - 300) / 520)} />
      </G>
      <Phase f={f} at={c.s3_timeout} until={c.request_votes}>
        <RibbonSeg x1={920} x2={1780} label="term 2" />
        <RibbonBlock x1={920} x2={1160} kind="election" />
      </Phase>
      <Phase f={f} at={c.heartbeats} until={c.leader_crash}>
        {HB_X.map((x) => (
          <Fan key={x} f={f} at={hbFrame(x)} x={x} from={LANE_Y.S1} to={FOLLOWER_LANES} dx={HB_DX} color={t.leader} dur={20} />
        ))}
        <Label x={LANE_X2} y={905} size={28} weight={600} anchor="end">
          election timeout: losowo 150–300 ms
        </Label>
      </Phase>
      {FOLLOWERS.map((s) => {
        const start = timerStart(X);
        const active = s === "S3" ? f >= c.leader_crash && f < c.request_votes : f >= c.leader_crash && f < c.s3_timeout;
        const op = f < (s === "S3" ? c.request_votes : c.s3_timeout) ? 1 : DIM;
        return (
          <G key={s} opacity={op} glow={active}>
            <TimerBar x={start} y={LANE_Y[s]} w={T[s]} progress={Math.min(1, (X - start) / T[s])} />
          </G>
        );
      })}
      <Phase f={f} at={c.s3_timeout} until={c.request_votes}>
        <Dot x={940} y={y3} role="candidate" />
        <Badge x={850} y={y3 - 52} text="term 2" size={24} stroke={t.c3} />
        <Check x={900} y={y3 + 48} s={16} />
      </Phase>
      <Phase f={f} at={c.request_votes} until={c.majority_votes}>
        <Fan
          f={f}
          at={c.request_votes}
          x={955}
          from={y3}
          to={[LANE_Y.S1, LANE_Y.S2, LANE_Y.S4, LANE_Y.S5]}
          dx={50}
          color={t.candidate}
          dashed={[LANE_Y.S1]}
        />
        <Label x={1030} y={410} size={26} weight={600} mono anchor="start">
          RequestVote
        </Label>
      </Phase>
      <Phase f={f} at={c.majority_votes} until={c.new_leader}>
        {(["S2", "S4"] as Server[]).map((s) => (
          <g key={s}>
            <Shot f={f} at={c.majority_votes} x1={1050} y1={LANE_Y[s]} x2={1130} y2={y3 + (LANE_Y[s] < y3 ? -16 : 16)} color={t.success} dur={12} />
            <Check x={1050} y={LANE_Y[s]} s={16} />
          </g>
        ))}
        <g opacity={progress(f, c.majority_votes + 10, 8)}>
          <Badge x={1290} y={y3 - 52} text="3/5 – większość" size={26} mono={false} stroke={t.heading} />
        </g>
      </Phase>
      <Phase f={f} at={c.new_leader}>
        <RibbonBlock x1={1154} x2={1780} kind="leader" p={progress(f, c.new_leader, 30)} />
        <Dot x={1170} y={y3} role="leader" />
        {[1480, 1660].map((x, i) => (
          <Fan key={x} f={f} at={c.new_leader + 12 + i * 20} x={x} from={y3} to={[LANE_Y.S2, LANE_Y.S4, LANE_Y.S5]} dx={50} color={t.leader} />
        ))}
      </Phase>
    </g>
  );
};

const electionCues = (cue: (n: string) => number): ElectionCues => ({
  heartbeats: cue("heartbeats"),
  leader_crash: cue("leader_crash"),
  s3_timeout: cue("s3_timeout"),
  request_votes: cue("request_votes"),
  majority_votes: cue("majority_votes"),
  new_leader: cue("new_leader"),
});

const Election: FC = () => {
  const { frame, cue } = useScene();
  return (
    <Diagram>
      <ElectionView f={frame} c={electionCues(cue)} />
    </Diagram>
  );
};

// ---------------------------------------------------------------- split_vote

const RewindIcon = ({ x, y }: { x: number; y: number }) => {
  const t = useTheme();
  return (
    <g fill={t.heading}>
      <polygon points={`${x},${y} ${x + 16},${y - 11} ${x + 16},${y + 11}`} />
      <polygon points={`${x + 16},${y} ${x + 32},${y - 11} ${x + 32},${y + 11}`} />
    </g>
  );
};

const SplitView = ({ f, c }: { f: number; c: Record<string, number> }) => {
  const t = useTheme();
  const T: Record<Server, number> = { S1: 0, S2: 190, S3: 260, S4: 185, S5: 280 };
  const X = 820 + 95 * linear(f, c.rewind + 15, Math.min(60, c.double_timeout - c.rewind - 15));
  const D = c.s4_wins - c.random_retry;
  const k = (x: number) => c.random_retry + D * x;
  const X2 = 1200 + 160 * linear(f, c.random_retry, D * 0.3);
  const s4Timeout = k(0.32);
  const s4Votes = k(0.4);
  const s4Granted = k(0.65);
  const s2Role: Role = f >= c.double_timeout && f < s4Votes + 20 ? "candidate" : "follower";
  const s4Role: Role = f >= c.s4_wins ? "leader" : f >= c.double_timeout ? "candidate" : "follower";
  const y2 = LANE_Y.S2;
  const y4 = LANE_Y.S4;
  const retryAfter = f >= c.random_retry;
  return (
    <g>
      <Lanes roles={{ S1: "crashed", S2: s2Role, S4: s4Role }} />
      <G opacity={DIM}>
        <RibbonSeg x1={300} x2={892} label="term 1" />
        <RibbonBlock x1={300} x2={820} kind="leader" />
        {HB_X.map((x) => (
          <Fan key={x} f={1} at={0} x={x} from={LANE_Y.S1} to={FOLLOWER_LANES} dx={HB_DX} color={t.leader} dur={1} />
        ))}
      </G>
      <G opacity={f < c.double_timeout ? 1 : DIM}>
        {FOLLOWERS.map((s) => {
          if ((s === "S2" || s === "S4") && f >= c.random_retry) return null;
          const start = hbArrive(HB_X[HB_X.length - 1]);
          return <TimerBar key={s} x={start} y={LANE_Y[s]} w={T[s]} progress={Math.min(1, (X - start) / T[s])} />;
        })}
      </G>
      <G opacity={f < c.no_majority ? opacityAt(f, c.double_timeout, c.split_votes) : f < c.random_retry ? 1 : DIM} glow={f >= c.no_majority && f < c.random_retry}>
        <RibbonSeg x1={900} x2={1352} label="term 2" />
        <RibbonBlock x1={900} x2={1352} kind="election" p={progress(f, c.double_timeout, 20)} />
        <g opacity={progress(f, c.no_majority, 12)}>
          <Cross x={1126} y={RIBBON_Y} s={22} />
          <Label x={1126} y={RIBBON_Y + 64} size={28} weight={700}>
            brak większości
          </Label>
        </g>
      </G>
      <Phase f={f} at={c.double_timeout} until={c.split_votes}>
        <Dot x={920} y={y2} role="candidate" />
        <Dot x={930} y={y4} role="candidate" />
        <Badge x={920} y={y2 - 54} text="term 2" size={24} stroke={t.c3} />
        <Badge x={930} y={y4 - 54} text="term 2" size={24} stroke={t.c3} />
      </Phase>
      <Phase f={f} at={c.split_votes} until={c.no_majority}>
        <Shot f={f} at={c.split_votes} x1={1060} y1={LANE_Y.S3} x2={948} y2={y2 + 18} color={t.success} dur={24} />
        <Shot f={f} at={c.split_votes + 10} x1={1060} y1={LANE_Y.S5} x2={958} y2={y4 + 18} color={t.success} dur={24} />
        <Check x={1060} y={LANE_Y.S3} s={16} />
        <Check x={1060} y={LANE_Y.S5} s={16} />
        <g opacity={progress(f, c.split_votes + 36, 12)}>
          <Badge x={1130} y={y2} text="2/5" size={26} stroke={t.heading} />
          <Badge x={1130} y={y4} text="2/5" size={26} stroke={t.heading} />
        </g>
      </Phase>
      <Phase f={f} at={c.random_retry} until={s4Timeout}>
        {retryAfter ? (
          <>
            <TimerBar x={1200} y={y2} w={260} progress={(X2 - 1200) / 260} />
            <TimerBar x={1200} y={y4} w={160} progress={(X2 - 1200) / 160} />
          </>
        ) : null}
      </Phase>
      {/* Fully gone once S4 times out: the candidate dot and the vote marks land where these labels sit. */}
      <G opacity={progress(f, c.random_retry, 12) * (1 - progress(f, s4Timeout, 10))} glow={f >= c.random_retry && f < s4Timeout}>
        <Label x={1480} y={y2 + 9} size={24} anchor="start" color={t.muted}>
          losowo
        </Label>
        <Label x={1380} y={y4 + 9} size={24} anchor="start" color={t.muted}>
          losowo
        </Label>
      </G>
      <Phase f={f} at={s4Timeout} until={s4Votes}>
        <RibbonSeg x1={1360} x2={1780} label="term 3" />
        <RibbonBlock x1={1360} x2={1580} kind="election" />
        <Dot x={1382} y={y4} role="candidate" />
      </Phase>
      <Phase f={f} at={s4Votes} until={s4Granted}>
        <Fan
          f={f}
          at={s4Votes}
          x={1395}
          from={y4}
          to={[LANE_Y.S1, y2, LANE_Y.S3, LANE_Y.S5]}
          dx={50}
          color={t.candidate}
          dashed={[LANE_Y.S1]}
        />
      </Phase>
      <Phase f={f} at={s4Granted} until={c.s4_wins}>
        {(
          [
            ["S2", 1500, 1540],
            ["S3", 1560, 1580],
            ["S5", 1500, 1540],
          ] as [Server, number, number][]
        ).map(([s, x, x2]) => (
          <g key={s}>
            <Shot f={f} at={s4Granted} x1={x} y1={LANE_Y[s]} x2={x2} y2={y4 + (LANE_Y[s] < y4 ? -18 : 18)} color={t.success} dur={24} />
            <Check x={x} y={LANE_Y[s]} s={16} />
          </g>
        ))}
      </Phase>
      <Phase f={f} at={c.s4_wins}>
        <RibbonBlock x1={1574} x2={1780} kind="leader" p={progress(f, c.s4_wins, 24)} />
        <Dot x={1620} y={y4} role="leader" />
        <Badge x={1716} y={y4} text="4/5" size={26} stroke={t.heading} />
      </Phase>
      <G opacity={progress(f, c.rewind, 12) * (1 - progress(f, c.double_timeout, 12))} glow={f >= c.rewind && f < c.double_timeout}>
        <RewindIcon x={1404} y={RIBBON_Y + 62} />
        <Label x={1450} y={RIBBON_Y + 72} size={28} weight={700} anchor="start">
          cofamy do awarii S1
        </Label>
      </G>
    </g>
  );
};

const SplitVote: FC = () => {
  const { frame: f, cue } = useScene();
  const c = {
    rewind: cue("rewind"),
    double_timeout: cue("double_timeout"),
    split_votes: cue("split_votes"),
    no_majority: cue("no_majority"),
    random_retry: cue("random_retry"),
    s4_wins: cue("s4_wins"),
  };
  const out = progress(f, c.rewind, 12);
  // The election scene's final frame, frozen, so the cut from `election` is seamless before the rewind.
  const held: ElectionCues = { heartbeats: -600, leader_crash: -400, s3_timeout: -300, request_votes: -200, majority_votes: -100, new_leader: -50 };
  return (
    <Diagram>
      {out < 1 ? (
        <G opacity={1 - out}>
          <ElectionView f={0} c={held} />
        </G>
      ) : null}
      <G opacity={out}>
        <SplitView f={f} c={c} />
      </G>
    </Diagram>
  );
};

export const scenes: Record<string, FC> = {
  key_insight: KeyInsight,
  server_states: ServerStates,
  terms: Terms,
  election: Election,
  split_vote: SplitVote,
};
