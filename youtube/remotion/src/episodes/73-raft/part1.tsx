import { useContext, type FC, type ReactNode } from "react";
import { AbsoluteFill } from "remotion";
import {
  Badge,
  Box,
  Card,
  Check,
  Cross,
  DIM,
  Diagram,
  G,
  Label,
  Link,
  MONO,
  RoleNode,
  SceneContext,
  SceneTitle,
  Serif,
  TermCard,
  Text,
  TitleCard,
  along,
  enter,
  focusOpacity,
  linear,
  progress,
  useScene,
  useTheme,
  type Role,
} from "../../design";
import { NODE_R, RING, SERVERS, type Server } from "./layout";

/** Chain of opacity/number targets: starts at steps[0][1], crossfades to each next value at its frame. */
const phased = (frame: number, steps: [number, number][]): number =>
  steps.slice(1).reduce((v, [at, val]) => v + (val - v) * progress(frame, at, 10), steps[0][1]);

const Node = ({ s, from, to, at }: { s: Server; from: Role; to?: Role; at?: number }) => {
  const { frame } = useScene();
  const [x, y] = RING[s];
  const p = to && at !== undefined ? progress(frame, at, 10) : 0;
  return (
    <g>
      <G opacity={1 - p}>
        <RoleNode x={x} y={y} label={s} role={from} r={NODE_R} />
      </G>
      {to && p > 0 ? (
        <G opacity={p}>
          <RoleNode x={x} y={y} label={s} role={to} r={NODE_R} />
        </G>
      ) : null}
    </g>
  );
};

type CellLook = "empty" | "filled" | "pending" | "committed" | "conflict";

const MiniCell = ({ x, y, w, h = 48, cmd, look }: { x: number; y: number; w: number; h?: number; cmd?: string; look: CellLook }) => {
  const t = useTheme();
  const fill = look === "committed" ? t.successSoft : look === "empty" ? "none" : t.surface;
  const stroke =
    look === "committed" ? t.success : look === "conflict" ? t.danger : look === "empty" ? t.line : t.muted;
  const dash = look === "empty" || look === "pending" ? "8 6" : undefined;
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={10} fill={fill} stroke={stroke} strokeWidth={3} strokeDasharray={dash} />
      {cmd ? (
        <Label x={x + w / 2} y={y + h / 2 + 9} size={24} weight={700} mono color={look === "conflict" ? t.danger : t.ink}>
          {cmd}
        </Label>
      ) : null}
      {look === "committed" ? <Check x={x + w - 4} y={y + 4} s={13} /> : null}
      {look === "conflict" ? <Cross x={x + w - 4} y={y + 4} s={16} /> : null}
    </g>
  );
};

const CLIENT: [number, number] = [1690, 320];

const ClientChip = ({ opacity = 1 }: { opacity?: number }) => {
  const t = useTheme();
  return (
    <G opacity={opacity}>
      <rect x={CLIENT[0] - 100} y={CLIENT[1] - 34} width={200} height={68} rx={34} fill={t.surface} stroke={t.muted} strokeWidth={3} />
      <Label x={CLIENT[0]} y={CLIENT[1] + 10} size={30} weight={700}>
        Klient
      </Label>
    </G>
  );
};

const mesh = (): [Server, Server][] =>
  SERVERS.flatMap((a, i) => SERVERS.slice(i + 1).map((b) => [a, b] as [Server, Server]));

// ---------------------------------------------------------------- intro

const Intro: FC = () => {
  const { frame, cue } = useScene();
  const at = cue("teaser_ring");
  // The title card has its own ring art; it fades out completely before the teaser ring enters.
  const card = 1 - progress(frame, at, 10);
  return (
    <AbsoluteFill>
      {card > 0 ? (
        <AbsoluteFill style={{ opacity: card }}>
          <TitleCard
            number={73}
            title="Raft"
            subtitle="W poszukiwaniu zrozumiałego algorytmu konsensusu"
            authors="Diego Ongaro, John Ousterhout · Stanford · 2014"
          />
        </AbsoluteFill>
      ) : null}
      <Diagram>
        {SERVERS.map((s, i) => (
          <G key={s} opacity={progress(frame, at + 8 + i * 2, 10)}>
            <RoleNode x={RING[s][0]} y={RING[s][1]} label={s} role="follower" r={NODE_R} />
          </G>
        ))}
      </Diagram>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- hook

const HOOK_CELL_W = 96;
const HOOK_STRIP: Record<Server, [number, number]> = {
  S1: [626, 272],
  S2: [1231, 483],
  S3: [1133, 784],
  S4: [467, 784],
  S5: [369, 483],
};

const Hook: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const off = cue("s5_offline");
  const ok = cue("write_ok");
  const crash = cue("leader_crash");
  const stale = cue("stale_leader");
  const ow = cue("overwrite");

  // The narration describes the write ("Klient wysyła…", "S jeden kopiuje…") before the write_ok cue,
  // at fixed offsets after s5_offline measured from the TTS timing; the copy is done by write_ok.
  const send = off + 89;
  const okLand = send + 24;
  const copy = Math.min(off + 225, ok - 40);
  const copyDone = copy + 22;
  const owDone = ow + 24;

  const op: Record<Server, number> = {
    S1: phased(frame, [[0, 1], [crash, 1], [stale, DIM]]),
    S2: phased(frame, [[0, 1], [crash, DIM], [ow, 1]]),
    S3: phased(frame, [[0, 1], [crash, DIM], [ow, 1]]),
    S4: phased(frame, [[0, 1], [send, DIM], [ow, 1]]),
    S5: phased(frame, [[0, 1], [off, DIM], [stale, 1]]),
  };
  const offline = (s: Server) =>
    (s === "S5" && frame >= off && frame < stale) || (s === "S1" && frame >= crash);

  const cell2 = (s: Server): { cmd?: string; look: CellLook } => {
    if (frame >= owDone && (s === "S2" || s === "S3")) return { cmd: "x←9", look: s === "S2" ? "conflict" : "pending" };
    if (frame >= owDone && s === "S4") return { cmd: "x←9", look: "pending" };
    if (frame >= ow && s === "S5") return { cmd: "x←9", look: "pending" };
    if (s === "S1" && frame >= okLand) return { cmd: "x←5", look: frame >= ok ? "committed" : "pending" };
    if ((s === "S2" || s === "S3") && frame >= copyDone) return { cmd: "x←5", look: frame >= ok ? "committed" : "pending" };
    return { look: "empty" };
  };

  const glowCell = (s: Server) =>
    (frame >= okLand && frame < crash && s === "S1") ||
    (frame >= copyDone && frame < crash && (s === "S2" || s === "S3")) ||
    (frame >= owDone && s === "S2");

  const clientOp = phased(frame, [[0, 1], [crash, DIM], [ow, 1]]);
  const s1 = RING.S1;
  const s5 = RING.S5;

  return (
    <Diagram>
      <Badge x={240} y={190} text="naiwny algorytm" mono={false} textColor={t.muted} />
      {mesh().map(([a, b]) => (
        <Link
          key={a + b}
          x1={RING[a][0]}
          y1={RING[a][1]}
          x2={RING[b][0]}
          y2={RING[b][1]}
          dashed={offline(a) || offline(b)}
          opacity={Math.min(op[a], op[b])}
        />
      ))}
      <ClientChip opacity={clientOp} />
      <G opacity={clientOp} glow={frame >= owDone}>
        <g opacity={progress(frame, ok, 10)}>
          <Badge x={CLIENT[0]} y={CLIENT[1] + 78} text="OK ✓" color={t.successSoft} stroke={t.success} />
        </g>
      </G>
      {SERVERS.map((s) => {
        const [sx, sy] = HOOK_STRIP[s];
        const c2 = cell2(s);
        return (
          <G key={s} opacity={op[s]}>
            <G glow={(s === "S1" && frame >= crash && frame < stale) || (s === "S5" && frame >= stale && frame < ow)}>
              {s === "S1" ? <Node s="S1" from="leader" to="crashed" at={crash} /> : null}
              {s === "S5" ? <Node s="S5" from="follower" to="leader" at={stale} /> : null}
              {s !== "S1" && s !== "S5" ? <Node s={s} from="follower" /> : null}
            </G>
            <MiniCell x={sx} y={sy} w={HOOK_CELL_W} cmd="x←1" look="committed" />
            <G glow={glowCell(s)}>
              <MiniCell x={sx + HOOK_CELL_W + 8} y={sy} w={HOOK_CELL_W} cmd={c2.cmd} look={c2.look} />
            </G>
          </G>
        );
      })}
      <Arrow0 frame={frame} at={send} />
      {(["S2", "S3"] as Server[]).map((s) => {
        const [x, y] = edgeAlong(s1, RING[s], linear(frame, copy, 22));
        return frame > copy && frame < copyDone ? <circle key={s} cx={x} cy={y} r={12} fill={t.leader} /> : null;
      })}
      {(["S2", "S3", "S4"] as Server[]).map((s) => {
        const [x, y] = edgeAlong(s5, RING[s], linear(frame, ow, 24));
        return frame > ow && frame < owDone ? <circle key={s} cx={x} cy={y} r={12} fill={t.leader} /> : null;
      })}
      <g style={enter(frame, owDone + 12)}>
        <Label x={1824} y={930} size={40} weight={700} anchor="end">
          Klient dostał OK. Zapis zniknął.
        </Label>
      </g>
    </Diagram>
  );
};

/** Point along a→b between the two node rims, so message dots never cover node labels. */
const edgeAlong = (a: [number, number], b: [number, number], p: number): [number, number] => {
  const d = Math.hypot(b[0] - a[0], b[1] - a[1]);
  const ux = (b[0] - a[0]) / d;
  const uy = (b[1] - a[1]) / d;
  const m = NODE_R + 14;
  return along(a[0] + ux * m, a[1] + uy * m, b[0] - ux * m, b[1] - uy * m, p);
};

/** Client → S1 command dot for the hook write. */
const Arrow0 = ({ frame, at }: { frame: number; at: number }) => {
  const t = useTheme();
  const p = linear(frame, at, 24);
  if (p <= 0 || p >= 1) return null;
  const [x, y] = along(CLIENT[0] - 100, CLIENT[1], RING.S1[0] + NODE_R + 50, RING.S1[1], p);
  return <Badge x={x} y={y} text="x←5" color={t.surface} stroke={t.heading} />;
};

// ---------------------------------------------------------------- replicated_log

const RL_CELL_W = 80;
const RL_UNIT: Record<Server, [number, number]> = {
  S1: [570, 226],
  S2: [1231, 451],
  S3: [1133, 752],
  S4: [411, 752],
  S5: [313, 451],
};
const RL_CMDS = ["x←3", "y←1", "x←2"];
const SYSTEMS = ["Chubby", "ZooKeeper", "GFS", "HDFS", "RAMCloud"];
// Badge width formula from the design system (sans, size 26), packed with a fixed gap and centered on the ring.
const SYSTEM_W = SYSTEMS.map((n) => Math.max(26 * 1.7, n.length * 26 * 0.58 + 26 * 1.2));
const SYSTEM_GAP = 28;
const SYSTEM_X = SYSTEM_W.map((w, i) => {
  const total = SYSTEM_W.reduce((a, b) => a + b, 0) + SYSTEM_GAP * (SYSTEMS.length - 1);
  const before = SYSTEM_W.slice(0, i).reduce((a, b) => a + b, 0) + SYSTEM_GAP * i;
  return RING.S1[0] - total / 2 + before + w / 2;
});

const ReplicatedLog: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cc = cue("client_command");
  const so = cue("same_order");
  const ss = cue("same_state");
  const tf = cue("two_failures");
  const rs = cue("real_systems");

  const failed = (s: Server) => s === "S4" || s === "S5";
  const nodeOp = (s: Server) => (failed(s) ? phased(frame, [[0, 1], [tf, DIM]]) : 1);
  const logOp = phased(frame, [[0, 1], [ss, DIM], [tf, 1]]);
  const stateOp = phased(frame, [[0, 1], [cc, DIM], [ss, 1]]);
  const clientOp = phased(frame, [[0, 1], [so, DIM]]);
  const units = progress(frame, 0, 15);

  return (
    <>
      <Diagram>
        {mesh().map(([a, b]) => (
          <Link
            key={a + b}
            x1={RING[a][0]}
            y1={RING[a][1]}
            x2={RING[b][0]}
            y2={RING[b][1]}
            dashed={frame >= tf && (failed(a) || failed(b))}
            opacity={Math.min(nodeOp(a), nodeOp(b))}
          />
        ))}
        <G opacity={clientOp} glow={frame >= cc && frame < so}>
          <ClientChip />
        </G>
        {RL_CMDS.map((cmd, i) => {
          const p = linear(frame, cc + i * 30, 24);
          if (p <= 0 || p >= 1) return null;
          const [x, y] = along(CLIENT[0] - 100, CLIENT[1], RING.S1[0] + NODE_R, RING.S1[1], p);
          return <Badge key={cmd} x={x} y={y} text={cmd} color={t.surface} stroke={t.heading} />;
        })}
        {SERVERS.map((s) => {
          const [ux, uy] = RL_UNIT[s];
          const op = nodeOp(s);
          return (
            <G key={s} opacity={op}>
              <Node s={s} from="follower" to={failed(s) ? "crashed" : undefined} at={tf} />
              <g opacity={units}>
                <G opacity={logOp} glow={frame >= so && frame < ss && !failed(s)}>
                  {RL_CMDS.map((cmd, i) => {
                    const on = frame >= so + i * 15;
                    return (
                      <MiniCell
                        key={cmd}
                        x={ux + i * (RL_CELL_W + 8)}
                        y={uy}
                        w={RL_CELL_W}
                        h={52}
                        cmd={on ? cmd : undefined}
                        look={on ? "filled" : "empty"}
                      />
                    );
                  })}
                </G>
                <G opacity={stateOp} glow={frame >= ss && frame < tf}>
                  <rect x={ux} y={uy + 60} width={RL_CELL_W * 3 + 16} height={52} rx={10} fill={t.inset} stroke={t.line} strokeWidth={2} />
                  <g opacity={progress(frame, ss, 12)}>
                    <Label x={ux + (RL_CELL_W * 3 + 16) / 2} y={uy + 95} size={26} weight={700} mono>
                      x=2, y=1
                    </Label>
                  </g>
                </G>
              </g>
            </G>
          );
        })}
        {SYSTEMS.map((name, i) => {
          const x = SYSTEM_X[i];
          return (
            <g key={name} style={enter(frame, rs + i * 8)}>
              <Badge x={x} y={925} text={name} mono={false} textColor={t.muted} />
            </g>
          );
        })}
      </Diagram>
      <Box x={1224} y={196} w={600} style={{ textAlign: "right", ...enter(frame, tf + 10) }}>
        <Text size={32} weight={700}>
          5 serwerów → przeżywa 2 awarie
        </Text>
      </Box>
    </>
  );
};

// ---------------------------------------------------------------- paxos_problem

const Chip = ({ children, active, opacity, style }: { children: ReactNode; active: boolean; opacity: number; style?: object }) => {
  const t = useTheme();
  return (
    <div
      style={{
        display: "inline-block",
        padding: "10px 24px",
        borderRadius: 999,
        background: t.inset,
        border: `2px solid ${active ? t.heading : t.line}`,
        boxShadow: active ? `0 0 24px ${t.glow}` : undefined,
        opacity,
        ...style,
      }}
    >
      <Text size={30} weight={600}>
        {children}
      </Text>
    </div>
  );
};

const PaxosProblem: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const pc = cue("paxos_card");
  const ns = cue("nsdi_survey");
  const ys = cue("year_struggle");
  const cq = cue("chubby_quote");
  const rg = cue("raft_goal");
  // "a powszechnie uzgodnionego…" starts ~7.6 s after year_struggle (TTS timing); no cue exists for it.
  const noMulti = Math.min(ys + 228, cq - 45);

  const cardOp = phased(frame, [[0, 1], [cq, DIM]]);
  const diagOp = phased(frame, [[0, 1], [ns, DIM]]);
  const quoteOp = phased(frame, [[0, 1], [rg, DIM]]);
  const chips: { text: string; at: number; until: number }[] = [
    { text: "NSDI 2012: mało kto czuje się pewnie", at: ns, until: ys },
    { text: "autorzy: prawie rok nauki", at: ys, until: noMulti },
    { text: "brak uzgodnionego multi-Paxos", at: noMulti, until: Infinity },
  ];

  return (
    <>
      <div style={{ ...enter(frame, pc) }}>
        <Card x={96} y={160} w={960} h={590} opacity={cardOp} style={{ borderColor: t.muted }}>
          <Serif size={60}>Paxos</Serif>
          <svg width={896} height={170} viewBox="0 0 896 170" style={{ position: "absolute", left: 32, top: 116, opacity: diagOp, overflow: "visible" }}>
            <rect x={0} y={30} width={310} height={110} rx={18} fill={t.inset} stroke={t.muted} strokeWidth={3} />
            <Label x={155} y={95} size={30} weight={700} mono>
              single-decree
            </Label>
            <line x1={330} y1={85} x2={450} y2={85} stroke={t.muted} strokeWidth={4} strokeLinecap="round" />
            <polygon points="470,85 448,74 448,96" fill={t.muted} />
            {[2, 1, 0].map((k) => (
              <rect key={k} x={500 + k * 14} y={30 - k * 14} width={310} height={110} rx={18} fill={t.surface} stroke={t.muted} strokeWidth={3} />
            ))}
            <Label x={655} y={95} size={30} weight={700} mono>
              multi-Paxos
            </Label>
            <circle cx={846} cy={6} r={30} fill={t.inset} stroke={t.heading} strokeWidth={3} />
            <Label x={846} y={18} size={36} weight={800} color={t.heading}>
              ?
            </Label>
          </svg>
          <div style={{ position: "absolute", left: 32, top: 320, display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 18 }}>
            {chips.map((c) => {
              const e = enter(frame, c.at);
              const active = frame >= c.at && frame < c.until && frame < cq;
              return (
                <Chip key={c.text} active={active} opacity={e.opacity * focusOpacity(frame, c.at, c.until)} style={{ transform: e.transform }}>
                  {c.text}
                </Chip>
              );
            })}
          </div>
        </Card>
      </div>
      <Box x={96} y={780} w={960} style={{ ...enter(frame, cq), opacity: enter(frame, cq).opacity * quoteOp }}>
        <div style={{ borderLeft: `6px solid ${t.heading}`, paddingLeft: 32 }}>
          <Serif size={40} color={t.ink} style={{ fontWeight: 500, lineHeight: 1.25 }}>
            „the final system will be based on an unproven protocol”
          </Serif>
          <Text size={26} color={t.muted} mono style={{ marginTop: 14 }}>
            zespół Chubby · p.3
          </Text>
        </div>
      </Box>
      <div style={{ ...enter(frame, rg) }}>
        <Card x={1136} y={160} w={688} h={590} glow>
          <div style={{ position: "absolute", left: 56, right: 40, top: 150 }}>
            <Serif size={130}>Raft</Serif>
            <Text size={46} weight={700} style={{ marginTop: 36 }}>
              <span style={{ color: t.muted }}>Cel nr 1:</span> zrozumiałość
            </Text>
          </div>
        </Card>
      </div>
    </>
  );
};

// ---------------------------------------------------------------- glossary

const IconNode = ({ label, role }: { label: string; role: Role }) => <RoleNode x={158} y={120} label={label} role={role} r={62} />;

const LeaderIcon = () => {
  const t = useTheme();
  return (
    <g>
      <IconNode label="L" role="leader" />
      <polygon points="120,48 132,22 145,40 158,14 171,40 184,22 196,48" fill={t.leader} stroke={t.leader} strokeWidth={3} strokeLinejoin="round" />
    </g>
  );
};

const CandidateIcon = () => {
  const t = useTheme();
  return (
    <g>
      <IconNode label="C" role="candidate" />
      <g transform="translate(232 40)" fill={t.candidate}>
        {[0, 13, 26, 39].map((dx, i) => (
          <rect key={dx} x={dx} y={i === 0 || i === 3 ? 10 : 0} width={10} height={40} rx={5} />
        ))}
        <rect x={0} y={32} width={49} height={40} rx={14} />
      </g>
    </g>
  );
};

const TermIcon = () => {
  const t = useTheme();
  return (
    <g>
      <rect x={58} y={82} width={200} height={76} rx={38} fill={t.c3} />
      <text x={158} y={132} textAnchor="middle" style={{ fill: t.onRole, fontFamily: MONO, fontSize: 32, fontWeight: 700 }}>
        term 1
      </text>
    </g>
  );
};

const GLOSSARY: { cue: string; term: string; definition: string; icon: ReactNode }[] = [
  { cue: "term_leader", term: "Leader", definition: "przyjmuje zapisy i rozsyła log", icon: <LeaderIcon /> },
  { cue: "term_follower", term: "Follower", definition: "biernie odpowiada na żądania", icon: <IconNode label="F" role="follower" /> },
  { cue: "term_candidate", term: "Candidate", definition: "zbiera głosy, by zostać leaderem", icon: <CandidateIcon /> },
  { cue: "term_term", term: "Term", definition: "numerowana kadencja, logiczny zegar", icon: <TermIcon /> },
  { cue: "term_commit", term: "Commit", definition: "wpis bezpieczny do wykonania", icon: <Check x={158} y={120} s={62} /> },
];

const CARD_W = 320;
const CARD_H = 470;

const Glossary: FC = () => {
  const { frame, cue, duration } = useScene();
  const t = useTheme();
  const info = useContext(SceneContext);
  // Final hold (all cards at full opacity) starts when the skeptic's question begins.
  const hold = info.speakers.find((s) => s.speaker === "skeptic")?.from ?? duration;
  const holdP = progress(frame, hold, 10);
  const ats = GLOSSARY.map((g) => cue(g.cue));

  return (
    <>
      <SceneTitle>Pięć pojęć na cały odcinek</SceneTitle>
      {GLOSSARY.map((g, i) => {
        const x = 96 + i * (CARD_W + 32);
        const at = ats[i];
        const until = i + 1 < ats.length ? ats[i + 1] : hold;
        const op = Math.max(focusOpacity(frame, at, until), holdP);
        const active = frame >= at && frame < until;
        return (
          <div key={g.term} style={{ position: "absolute", inset: 0, opacity: op }}>
            <TermCard x={x} y={290} w={CARD_W} h={CARD_H} term={g.term} definition={g.definition} icon={g.icon} at={at} />
            {active ? (
              <div
                style={{
                  position: "absolute",
                  left: x,
                  top: 290,
                  width: CARD_W,
                  height: CARD_H,
                  boxSizing: "border-box",
                  borderRadius: 22,
                  border: `2px solid ${t.heading}`,
                  boxShadow: `0 0 28px ${t.glow}`,
                  opacity: progress(frame, at, 15),
                }}
              />
            ) : null}
          </div>
        );
      })}
    </>
  );
};

export const scenes: Record<string, FC> = {
  intro: Intro,
  hook: Hook,
  replicated_log: ReplicatedLog,
  paxos_problem: PaxosProblem,
  glossary: Glossary,
};
