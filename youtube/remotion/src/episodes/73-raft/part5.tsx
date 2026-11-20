import type { FC, ReactNode } from "react";
import {
  Arrow,
  Badge,
  Box,
  Card,
  Check,
  Cross,
  DIM,
  Diagram,
  G,
  Label,
  Lane,
  ListItem,
  LogCell,
  Link,
  MONO,
  Message,
  RoleNode,
  SceneTitle,
  Serif,
  Text,
  TimerBar,
  enter,
  focusOpacity,
  linear,
  progress,
  ring,
  useScene,
  useTheme,
  type Role,
} from "../../design";
import { LANE_X1, LANE_X2, LANE_Y, RIBBON_Y, SERVERS, type Server } from "./layout";

const between = (frame: number, a: number, b = Infinity) => frame >= a && frame < b;

const Pill = ({ children, border, glow = false }: { children: ReactNode; border?: string; glow?: boolean }) => {
  const t = useTheme();
  return (
    <div
      style={{
        display: "inline-block",
        padding: "12px 28px",
        borderRadius: 999,
        background: t.surface,
        border: `3px solid ${border ?? t.line}`,
        boxShadow: glow ? `0 0 28px ${t.glow}` : undefined,
        fontFamily: MONO,
        fontWeight: 700,
        fontSize: 28,
        color: t.ink,
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </div>
  );
};

// ---------------------------------------------------------------- user_study

const US_AXIS_X = 260;
const US_BASE = 880;
const US_TOP = 320;
const usY = (v: number) => US_BASE - ((US_BASE - US_TOP) * v) / 60;

const UserStudy: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const bars = cue("bars_means");
  const diff = cue("diff_label");
  const count = cue("participants_count");
  const bias = cue("bias_note");
  const survey = cue("survey");

  const pRaft = progress(frame, bars, 14);
  const pPaxos = pRaft;
  const valuesOp = progress(frame, bars + 4, 10);
  const raftTop = usY(25.7);
  const paxosTop = usY(20.8);
  const pDiff = progress(frame, diff, 15);

  return (
    <>
      <SceneTitle>Raft zrozumiany lepiej niż Paxos</SceneTitle>
      <Diagram>
        <G opacity={focusOpacity(frame, bars, count)}>
          {[0, 20, 40, 60].map((v) => (
            <g key={v}>
              <line x1={US_AXIS_X} y1={usY(v)} x2={1000} y2={usY(v)} stroke={t.line} strokeWidth={2} strokeDasharray={v === 0 ? undefined : "6 10"} />
              <Label x={US_AXIS_X - 20} y={usY(v) + 9} size={24} mono anchor="end" color={t.muted}>
                {v}
              </Label>
            </g>
          ))}
          <Label x={US_AXIS_X} y={285} size={26} anchor="start" color={t.muted}>
            punkty w quizie · n = 43
          </Label>
          <G glow={between(frame, bars, diff)}>
            <rect x={380} y={US_BASE - (US_BASE - raftTop) * pRaft} width={200} height={(US_BASE - raftTop) * pRaft} rx={10} fill={t.leader} />
            <rect x={680} y={US_BASE - (US_BASE - paxosTop) * pPaxos} width={200} height={(US_BASE - paxosTop) * pPaxos} rx={10} fill={t.muted} />
          </G>
          <Label x={480} y={raftTop + 56} size={44} mono weight={700} color={t.onRole} opacity={valuesOp}>
            25,7
          </Label>
          <Label x={780} y={paxosTop + 56} size={44} mono weight={700} color={t.onRole} opacity={valuesOp}>
            20,8
          </Label>
          <Label x={480} y={928} size={34} weight={700}>
            Raft
          </Label>
          <Label x={780} y={928} size={34} weight={700}>
            Paxos
          </Label>
          <G opacity={pDiff} glow={between(frame, diff, count)}>
            <line x1={580} y1={raftTop} x2={930} y2={raftTop} stroke={t.heading} strokeWidth={3} strokeDasharray="8 8" />
            <path
              d={`M905 ${raftTop} H920 V${paxosTop} H905`}
              fill="none"
              stroke={t.heading}
              strokeWidth={4}
              strokeLinejoin="round"
            />
            <Label x={940} y={(raftTop + paxosTop) / 2 + 12} size={34} weight={700} anchor="start" color={t.heading}>
              +4,9 pkt
            </Label>
          </G>
        </G>
      </Diagram>

      <div style={{ ...enter(frame, count) }}>
        <Card x={1160} y={250} w={660} h={250} glow={between(frame, count, bias)} opacity={focusOpacity(frame, count, bias)}>
          <Serif size={130}>33 z 43</Serif>
          <Text size={32} color={t.muted} style={{ marginTop: 10 }}>
            lepszy wynik z Rafta
          </Text>
        </Card>
      </div>

      <div style={{ ...enter(frame, bias) }}>
        <Card x={1160} y={530} w={660} h={170} glow={between(frame, bias, survey)} opacity={focusOpacity(frame, bias, survey)}>
          <Text size={30} color={t.muted}>
            15 z 43 znało Paxos
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 8 }}>
            wykład Paxos 14% dłuższy
          </Text>
        </Card>
      </div>

      <div style={{ ...enter(frame, survey) }}>
        <Card x={1160} y={730} w={660} h={200} glow={frame >= survey} opacity={focusOpacity(frame, survey)}>
          <Text size={34} weight={700}>
            ankieta: 33 z 41 · Raft łatwiejszy
          </Text>
          <div style={{ marginTop: 26, width: 596, height: 44, borderRadius: 12, background: t.inset }}>
            <div style={{ width: (596 * 33 * progress(frame, survey + 6, 24)) / 41, height: "100%", borderRadius: 12, background: t.leader }} />
          </div>
        </Card>
      </div>
    </>
  );
};

// ---------------------------------------------------------------- election_timing

const ET_X0 = 620;
const ET_DECADE = 330;
const etX = (ms: number) => ET_X0 + (Math.log10(ms) - 1) * ET_DECADE;
const ET_ROWS = [410, 540, 670, 800];
const ET_BAR_H = 52;

const TimingRow = ({
  y,
  label,
  value,
  ms,
  at,
  until,
  color,
  outline = false,
  children,
}: {
  y: number;
  label: string;
  value: string;
  ms: number;
  at: number;
  until: number;
  color: string;
  outline?: boolean;
  children?: ReactNode;
}) => {
  const { frame } = useScene();
  const t = useTheme();
  const p = progress(frame, at, 24);
  const w = (etX(ms) - ET_X0) * p;
  const shown = frame >= at ? 1 : 0;
  return (
    <G opacity={shown * focusOpacity(frame, at, until)} glow={between(frame, at, until)}>
      <Label x={570} y={y + 11} size={32} mono weight={700} anchor="end">
        {label}
      </Label>
      <rect
        x={ET_X0}
        y={y - ET_BAR_H / 2}
        width={w}
        height={ET_BAR_H}
        rx={10}
        fill={outline ? t.surface : color}
        stroke={outline ? color : "none"}
        strokeWidth={4}
        strokeDasharray={outline ? "10 8" : undefined}
      />
      <Label x={ET_X0 + 20} y={y - ET_BAR_H / 2 - 16} size={28} weight={700} anchor="start" opacity={p}>
        {value}
      </Label>
      <g opacity={p}>{children}</g>
    </G>
  );
};

const ElectionTiming: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const setup = cue("setup");
  const noRandom = cue("no_random");
  const fiveMs = cue("five_ms");
  const worst = cue("fifty_ms_worst");
  const short = cue("short_timeouts");
  const rec = cue("recommendation");

  return (
    <>
      <SceneTitle>5 ms losowości zamiast ponad 10 s przestoju</SceneTitle>
      <Box x={96} y={222} style={{ ...enter(frame, setup), opacity: enter(frame, setup).opacity * focusOpacity(frame, setup, noRandom) }}>
        <Pill border={between(frame, setup, noRandom) ? t.heading : undefined} glow={between(frame, setup, noRandom)}>
          5 serwerów · broadcast ≈15 ms · 1000 prób
          <span style={{ fontSize: 22, color: t.muted, marginLeft: 14 }}>(100 dla 150–150 ms)</span>
        </Pill>
      </Box>
      <div style={{ position: "absolute", right: 96, top: 222, ...enter(frame, rec) }}>
        <Pill border={t.heading} glow={frame >= rec}>
          zalecane: 150–300 ms
        </Pill>
      </div>
      <Diagram>
        <G opacity={progress(frame, setup, 15) * (frame >= rec ? DIM + (1 - DIM) * (1 - progress(frame, rec, 10)) : 1)}>
          <Label x={570} y={330} size={24} anchor="end" color={t.muted}>
            election timeout
          </Label>
          <Label x={1720} y={330} size={24} anchor="end" color={t.muted}>
            czas wyboru leadera (skala log.)
          </Label>
          {[10, 100, 1000, 10000].map((v) => (
            <g key={v}>
              <line x1={etX(v)} y1={v === 10 ? 350 : 846} x2={etX(v)} y2={862} stroke={t.line} strokeWidth={v === 10 ? 2 : 3} />
              <Label x={etX(v)} y={892} size={24} mono color={t.muted}>
                {v === 10000 ? "10 000 ms" : String(v)}
              </Label>
            </g>
          ))}
        </G>
        <TimingRow y={ET_ROWS[0]} label="150–150 ms" value="> 10 000 ms · split votes" ms={10000} at={noRandom} until={fiveMs} color={t.muted}>
          <Arrow x1={etX(10000)} y1={ET_ROWS[0]} x2={1730} y2={ET_ROWS[0]} color={t.muted} width={5} dashed />
        </TimingRow>
        <TimingRow y={ET_ROWS[1]} label="150–155 ms" value="mediana 287 ms" ms={287} at={fiveMs} until={worst} color={t.leader} />
        <TimingRow y={ET_ROWS[2]} label="150–200 ms" value="najgorszy z 1000 prób: 513 ms" ms={513} at={worst} until={short} color={t.leader} outline />
        <TimingRow y={ET_ROWS[3]} label="12–24 ms" value="średnio 35 ms" ms={35} at={short} until={rec} color={t.leader}>
          <Label x={etX(35) + 40} y={ET_ROWS[3] + 10} size={28} anchor="start" color={t.muted}>
            za krótki: łamie wymaganie czasowe
          </Label>
        </TimingRow>
      </Diagram>
    </>
  );
};

// ---------------------------------------------------------------- limitations

const RIB_H = 44;
const RIB_X0 = 280;
const GAP_X1 = 1280;
const GAP_X2 = 1560;
const ELECTION_W = 30;

type Flip = { term: number; x: number; to: Server; prev: Server; timer: [number, number]; hb: [number, number] };
const FLIPS: Flip[] = [
  { term: 5, x: 560, to: "S2", prev: "S3", timer: [300, 200], hb: [300, 545] },
  { term: 6, x: 800, to: "S4", prev: "S2", timer: [660, 110], hb: [600, 785] },
  { term: 7, x: 1040, to: "S2", prev: "S4", timer: [900, 110], hb: [840, 1025] },
];
// Continues from split_vote, which ended in term 3; the re-run starts in the next term.
const RERUN_TERM = 4;
// Short timers on the other followers; slightly slower than S2's so S2 fires first.
const SIDE_TIMERS: { s: Server; dur: number }[] = [
  { s: "S1", dur: 175 },
  { s: "S4", dur: 185 },
  { s: "S5", dur: 195 },
];

const RibbonSeg = ({ x1, x2, term, opacity = 1 }: { x1: number; x2: number; term: number; opacity?: number }) => {
  const t = useTheme();
  return (
    <g opacity={opacity}>
      <rect x={x1} y={RIBBON_Y - RIB_H / 2} width={x2 - x1} height={RIB_H} rx={10} fill={t.surface} stroke={t.c3} strokeWidth={3} />
      <rect x={x1 + 3} y={RIBBON_Y - RIB_H / 2 + 3} width={ELECTION_W} height={RIB_H - 6} rx={7} fill={t.candidate} />
      <Label x={(x1 + x2 + ELECTION_W) / 2} y={RIBBON_Y + 9} size={24} mono weight={700}>
        {`term ${term}`}
      </Label>
    </g>
  );
};

const Limitations: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const r = cue("rerun_short");
  const s = cue("spurious_elections");
  const tr = cue("timing_rule");
  const dg = cue("downtime_gap");
  const ep = cue("epaxos_card");

  // Flip 1 runs slowly under the narration; flips 2–3 are the quick "terms jumping" burst.
  const timing = FLIPS.map((_, i) => {
    const start = i === 0 ? r : i === 1 ? s : s + 80;
    const timerDur = i === 0 ? 140 : 25;
    const hbDur = i === 0 ? 220 : 40;
    const flipAt = start + timerDur + 5;
    const leaderAt = i === 0 ? start + hbDur : flipAt + 12;
    return { start, timerDur, hbDur, flipAt, leaderAt };
  });

  const roleOf = (srv: Server): Role => {
    let leader: Server = "S3";
    let candidate: Server | null = null;
    FLIPS.forEach((f, i) => {
      if (frame >= timing[i].leaderAt) leader = f.to;
      else if (frame >= timing[i].flipAt) candidate = f.to;
    });
    if (srv === candidate && srv !== leader) return "candidate";
    return srv === leader ? "leader" : "follower";
  };

  const lanesOp = 1 - progress(frame, tr, 15);
  const ribbonOp = frame < dg ? 1 - (1 - DIM) * progress(frame, tr, 10) : focusOpacity(frame, dg, ep);
  const nextX = (i: number) => (i + 1 < FLIPS.length ? FLIPS[i + 1].x : GAP_X1);
  const nextAt = (i: number) => (i + 1 < FLIPS.length ? timing[i + 1].flipAt : timing[i].leaderAt + 40);
  const s3Bar = linear(frame, r, timing[0].flipAt - r);
  const gapP = linear(frame, dg, 30);

  return (
    <>
      <Diagram>
        <G opacity={lanesOp}>
          {SERVERS.map((srv) => (
            <Lane key={srv} y={LANE_Y[srv]} label={srv} role={roleOf(srv)} x1={LANE_X1} x2={LANE_X2} />
          ))}
          <rect x={RIB_X0} y={LANE_Y.S3 - 9} width={(FLIPS[0].x - RIB_X0) * s3Bar} height={18} rx={9} fill={t.leader} />
          <g opacity={(frame >= r ? 1 : 0) * (1 - progress(frame, timing[0].flipAt, 10))}>
            {SIDE_TIMERS.map(({ s: srv, dur }) => (
              <TimerBar key={srv} x={FLIPS[0].timer[0]} y={LANE_Y[srv]} w={FLIPS[0].timer[1]} progress={linear(frame, r, dur)} />
            ))}
          </g>
          {FLIPS.map((f, i) => {
            const tm = timing[i];
            const y = LANE_Y[f.to];
            const hbP = linear(frame, tm.start, tm.hbDur);
            const barP = linear(frame, tm.leaderAt, nextAt(i) - tm.leaderAt);
            const barX = f.x + ELECTION_W + 6;
            return (
              <g key={f.term}>
                <G glow={i === 0 && between(frame, tm.start, tm.leaderAt)} opacity={frame >= tm.start ? 1 : 0}>
                  <TimerBar x={f.timer[0]} y={y} w={f.timer[1]} progress={linear(frame, tm.start, tm.timerDur)} />
                </G>
                <Arrow x1={f.hb[0]} y1={LANE_Y[f.prev]} x2={f.hb[1]} y2={y} color={t.leader} width={3} dashed progress={hbP} />
                <Message x1={f.hb[0]} y1={LANE_Y[f.prev]} x2={f.hb[1]} y2={y} t={hbP} color={t.leader} />
                {frame >= tm.flipAt ? <rect x={f.x} y={y - 9} width={ELECTION_W} height={18} rx={9} fill={t.candidate} opacity={progress(frame, tm.flipAt, 10)} /> : null}
                <rect x={barX} y={y - 9} width={Math.max(0, (nextX(i) - barX) * barP)} height={18} rx={9} fill={t.leader} />
              </g>
            );
          })}
        </G>

        <G opacity={ribbonOp}>
          <RibbonSeg x1={RIB_X0} x2={FLIPS[0].x} term={RERUN_TERM} />
          <Label x={(RIB_X0 + FLIPS[0].x) / 2} y={182} size={24} color={t.muted} opacity={1 - progress(frame, s, 12)}>
            nowy przebieg
          </Label>
          {FLIPS.map((f, i) => (
            <RibbonSeg key={f.term} x1={f.x} x2={nextX(i)} term={f.term} opacity={progress(frame, timing[i].flipAt, 10)} />
          ))}
          <G glow={between(frame, s, tr)}>
            {FLIPS.map((f, i) => (
              <g key={f.term} opacity={progress(frame, timing[i].flipAt, 10)}>
                <Cross x={f.x} y={RIBBON_Y} s={18} />
              </g>
            ))}
          </G>
          <Label x={800} y={182} size={26} opacity={progress(frame, s, 15)}>
            zbędna zmiana leadera
          </Label>
        </G>

        <G opacity={frame >= dg ? 1 : 0} glow={between(frame, dg, ep)}>
          <g opacity={frame >= ep ? DIM + (1 - DIM) * (1 - progress(frame, ep, 10)) : 1}>
            <rect
              x={GAP_X1 + 6}
              y={RIBBON_Y - RIB_H / 2}
              width={(GAP_X2 - GAP_X1 - 12) * gapP}
              height={RIB_H}
              rx={10}
              fill={t.inset}
              stroke={t.muted}
              strokeWidth={3}
              strokeDasharray="9 7"
            />
            <Label x={(GAP_X1 + GAP_X2) / 2} y={182} size={26} opacity={progress(frame, dg, 15)}>
              przestój ≈ election timeout
            </Label>
            <RibbonSeg x1={GAP_X2} x2={LANE_X2} term={FLIPS[FLIPS.length - 1].term + 1} opacity={progress(frame, dg + 32, 10)} />
          </g>
        </G>
      </Diagram>

      <div style={{ opacity: frame >= tr ? enter(frame, tr).opacity : 0, transform: enter(frame, tr).transform }}>
        <Card x={300} y={340} w={1320} h={120} glow={between(frame, tr, dg)} opacity={focusOpacity(frame, tr, dg)} style={{ padding: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Text size={46} mono weight={700}>
            broadcastTime ≪ electionTimeout ≪ MTBF
          </Text>
        </Card>
        <Card x={300} y={500} w={640} h={170} opacity={focusOpacity(frame, tr, dg)}>
          <Text size={36} weight={700}>
            bezpieczeństwo
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 10 }}>
            <span style={{ color: t.success, fontWeight: 800 }}>✓</span> bez zależności od czasu
          </Text>
        </Card>
        <Card x={980} y={500} w={640} h={170} opacity={focusOpacity(frame, tr, ep)}>
          <Text size={36} weight={700}>
            dostępność
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 10 }}>
            zależy od czasu
          </Text>
        </Card>
      </div>

      <div style={{ ...enter(frame, ep) }}>
        <Card x={1100} y={730} w={720} h={170} glow={frame >= ep} opacity={frame >= ep ? 1 : 0}>
          <Text size={36} weight={700}>
            <span style={{ fontFamily: MONO }}>EPaxos</span> bez leadera
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 10 }}>
            niższa latencja w WAN
          </Text>
        </Card>
      </div>
    </>
  );
};

// ---------------------------------------------------------------- outro_invite

const OR_CX = 560;
const OR_CY = 470;
const OR_PTS = ring(OR_CX, OR_CY, 230, 5);
const OR_CELL_W = 130;
const OR_CELL_X = (i: number) => 290 + i * (OR_CELL_W + 14);
const OR_LOG_Y = 790;
const OR_LOG: { term: number; cmd: string; committed: boolean }[] = [
  { term: 1, cmd: "x←1", committed: true },
  { term: 1, cmd: "y←2", committed: true },
  { term: 2, cmd: "x←3", committed: true },
  { term: 2, cmd: "y←7", committed: true },
];
const RECAP = ["Wspólny log", "Losowy timeout", "Większość = commit", "Bieżący term", "33 z 43"];

const OutroInvite: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cues = ["recap_problem", "recap_election", "recap_log", "recap_safety", "recap_results"].map(cue);
  const [problem, election, log, safety, results] = cues;
  const next = cue("next_episode");

  const shown = progress(frame, problem, 18);
  const endDim = frame >= next ? 1 - (1 - DIM) * progress(frame, next, 12) : 1;
  const focus = (a: number, b: number) => (frame < election ? 1 : focusOpacity(frame, a, b));
  const leaderIdx = 2;
  const [lx, ly] = OR_PTS[leaderIdx];
  // Final S3 log from consistency_check: all four entries committed.
  const markerX = OR_CELL_X(3) + OR_CELL_W + 7;
  const slide = progress(frame, next, 20);

  return (
    <>
      <Diagram>
        <g opacity={shown * endDim}>
          <G opacity={focus(election, log)}>
            {OR_PTS.map(([x, y], i) => {
              if (i === leaderIdx) return null;
              const d = Math.hypot(x - lx, y - ly);
              const ux = (x - lx) / d;
              const uy = (y - ly) / d;
              return <Link key={i} x1={lx + ux * 56} y1={ly + uy * 56} x2={x - ux * 56} y2={y - uy * 56} />;
            })}
          </G>
          {OR_PTS.map(([x, y], i) => (
            <G key={i} opacity={i === leaderIdx ? focus(election, log) : frame < election ? 1 : DIM} glow={i === leaderIdx && between(frame, election, log)}>
              <RoleNode x={x} y={y} label={`S${i + 1}`} role={i === leaderIdx ? "leader" : "follower"} r={50} />
            </G>
          ))}
          <G opacity={focus(safety, results)} glow={between(frame, safety, results)}>
            <Badge x={lx + 140} y={ly} text="term 2" stroke={t.c3} />
          </G>
          <G opacity={frame < election ? 1 : DIM}>
            {OR_LOG.map((c, i) => (
              <LogCell key={i} x={OR_CELL_X(i)} y={OR_LOG_Y} w={OR_CELL_W} h={88} term={c.term} cmd={c.cmd} state={c.committed ? "committed" : "pending"} />
            ))}
          </G>
          <G opacity={focus(log, safety)} glow={between(frame, log, safety)}>
            <line x1={markerX} y1={OR_LOG_Y - 14} x2={markerX} y2={OR_LOG_Y + 102} stroke={t.success} strokeWidth={5} strokeLinecap="round" />
            <Check x={markerX} y={OR_LOG_Y - 36} s={20} />
            <Label x={markerX + 32} y={OR_LOG_Y - 27} size={26} mono anchor="start" color={t.success}>
              commit
            </Label>
          </G>
        </g>
      </Diagram>

      <Box x={1000} y={200} w={820} style={{ opacity: endDim }}>
        {RECAP.map((title, i) => (
          <ListItem
            key={title}
            index={i + 1}
            title={title}
            at={cues[i]}
            active={between(frame, cues[i], cues[i + 1] ?? next)}
            dim={frame >= (cues[i + 1] ?? Infinity)}
          />
        ))}
      </Box>

      {frame >= next ? (
        <div style={{ opacity: slide, transform: `translateX(${(1 - slide) * 320}px)` }}>
          <Card x={1000} y={740} w={820} h={190} glow>
            <Serif size={64}>Następny odcinek</Serif>
            <Text size={30} color={t.muted} style={{ marginTop: 14 }}>
              dziękujemy za wspólny odczyt
            </Text>
          </Card>
        </div>
      ) : null}
    </>
  );
};

export const scenes: Record<string, FC> = {
  user_study: UserStudy,
  election_timing: ElectionTiming,
  limitations: Limitations,
  outro_invite: OutroInvite,
};
