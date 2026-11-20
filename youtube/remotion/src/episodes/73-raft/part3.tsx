import type { FC, ReactNode } from "react";
import {
  Badge,
  Card,
  Check,
  CurvedArrow,
  DIM,
  Diagram,
  G,
  Label,
  LogCell,
  Message,
  RoleNode,
  Text,
  alongCurve,
  focusOpacity,
  linear,
  progress,
  useScene,
  useTheme,
  type CellState,
  type Role,
} from "../../design";
import {
  LOG_CELL_GAP,
  LOG_CELL_H,
  LOG_CELL_W,
  LOG_LABEL_X,
  LOG_ROW_Y,
  LOG_RULER_Y,
  logCellX,
  type Server,
} from "./layout";

const PANEL_X = 1240;
const PANEL_W = 580;
const MARKER_TOP = 282;
const MARKER_BOTTOM = 884;

type CellSpec = {
  i: number;
  term: number;
  cmd: string;
  state?: CellState;
  opacity?: number;
  glow?: boolean;
  dx?: number;
  dy?: number;
  check?: boolean;
};

const BASE: CellSpec[] = [
  { i: 1, term: 1, cmd: "x←1", state: "committed" },
  { i: 2, term: 1, cmd: "y←2", state: "committed" },
];

const rowMid = (s: Server) => LOG_ROW_Y[s] + LOG_CELL_H / 2;
const cellRight = (i: number) => logCellX(i) + LOG_CELL_W;
const markerX = (index: number) => logCellX(index) + LOG_CELL_W + LOG_CELL_GAP / 2;

const dimFrom = (frame: number, at: number) => 1 - (1 - DIM) * progress(frame, at, 10);
const anyFocus = (...values: number[]) => Math.max(...values);

// The marker slides one column right, staying visible, so the viewer sees commitIndex advance.
const markerSlide = (frame: number, at: number, from: number) => ({ index: from + progress(frame, at, 14), opacity: 1 });

const Row = ({ s, cells }: { s: Server; cells: CellSpec[] }) => (
  <>
    {cells.map((c) => (
      <G
        key={`${s}-${c.i}-${c.cmd}`}
        opacity={c.opacity ?? 1}
        glow={c.glow}
        transform={c.dx || c.dy ? `translate(${c.dx ?? 0} ${c.dy ?? 0})` : undefined}
      >
        <LogCell x={logCellX(c.i)} y={LOG_ROW_Y[s]} w={LOG_CELL_W} h={LOG_CELL_H} term={c.term} cmd={c.cmd} state={c.state} />
        {c.check ? <Check x={cellRight(c.i) - 20} y={LOG_ROW_Y[s] + 20} s={14} /> : null}
      </G>
    ))}
  </>
);

const Slot = ({ s, i, opacity = 1 }: { s: Server; i: number; opacity?: number }) => (
  <G opacity={opacity}>
    <LogCell x={logCellX(i)} y={LOG_ROW_Y[s]} w={LOG_CELL_W} h={LOG_CELL_H} state="empty" />
  </G>
);

const Ruler = ({ opacity = 1, highlight }: { opacity?: number; highlight?: number }) => {
  const t = useTheme();
  return (
    <G opacity={opacity}>
      <Label x={LOG_LABEL_X} y={LOG_RULER_Y + 12} size={24} color={t.muted} mono>
        index
      </Label>
      {[1, 2, 3, 4, 5].map((i) => (
        <Label key={i} x={logCellX(i) + LOG_CELL_W / 2} y={LOG_RULER_Y + 12} size={26} mono weight={700} color={i === highlight ? t.heading : t.muted}>
          {String(i)}
        </Label>
      ))}
    </G>
  );
};

const Node = ({ s, role, opacity = 1 }: { s: Server; role: Role; opacity?: number }) => (
  <G opacity={opacity}>
    <RoleNode x={LOG_LABEL_X} y={rowMid(s)} label={s} role={role} r={38} fontSize={24} />
  </G>
);

const CommitMarker = ({ index, opacity = 1, glow = false }: { index: number; opacity?: number; glow?: boolean }) => {
  const t = useTheme();
  const lo = Math.floor(index);
  const x = markerX(lo) + (markerX(lo + 1) - markerX(lo)) * (index - lo);
  return (
    <G opacity={opacity} glow={glow}>
      <line x1={x} y1={MARKER_TOP} x2={x} y2={MARKER_BOTTOM} stroke={t.success} strokeWidth={5} strokeLinecap="round" />
      <Badge x={x} y={912} text={`commitIndex = ${Math.round(index)}`} color={t.successSoft} stroke={t.success} size={24} />
    </G>
  );
};

const Hull = ({ x, y, w, h, opacity = 1, glow = true }: { x: number; y: number; w: number; h: number; opacity?: number; glow?: boolean }) => {
  const t = useTheme();
  return (
    <G opacity={opacity} glow={glow}>
      <rect x={x} y={y} width={w} height={h} rx={18} fill="none" stroke={t.heading} strokeWidth={4} />
    </G>
  );
};

const Fields = ({ title, lines, hot = [] }: { title: string; lines: string[]; hot?: number[] }) => {
  const t = useTheme();
  return (
    <>
      <Text size={26} weight={700} color={t.muted}>
        {title}
      </Text>
      {lines.map((l, i) => (
        <Text key={l} size={32} weight={hot.includes(i) ? 700 : 500} mono color={hot.includes(i) ? t.heading : t.ink} style={{ marginTop: 10 }}>
          {l}
        </Text>
      ))}
    </>
  );
};

const Fade = ({ opacity, dy = 0, children }: { opacity: number; dy?: number; children: ReactNode }) => (
  <div style={{ position: "absolute", inset: 0, opacity, transform: `translateY(${dy}px)` }}>{children}</div>
);

// Messages fan out from the leader cell's right edge so they never cross other cells.
const fan = (from: Server, to: Server, index: number, bulge: number) => {
  const x = cellRight(index) + 4;
  const y1 = rowMid(from);
  const y2 = rowMid(to);
  return { x1: x, y1, cx: x + bulge, cy: (y1 + y2) / 2, x2: x, y2 };
};

const LogAppend: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cClient = cue("client_request");
  const cAppend = cue("leader_append");
  const cAE = cue("append_entries");
  const cAck = cue("majority_ack");
  const cCommit = cue("commit_marker");
  const cApply = cue("followers_apply");

  const base = dimFrom(frame, cClient);
  const rowsAE = anyFocus(focusOpacity(frame, cAE, cAck), base * (frame < cAE ? 1 : 0));
  const s24 = anyFocus(focusOpacity(frame, cAE, cCommit), focusOpacity(frame, cApply), frame < cClient ? 1 : 0);
  const s5 = anyFocus(focusOpacity(frame, cAE, cAck), frame < cClient ? 1 : 0);

  // Narration opens with "S3 is leader in term 2" and its committed prefix; both stay readable until the append.
  const s3Base = anyFocus(base, focusOpacity(frame, -10, cAppend));
  const s3Tag = focusOpacity(frame, -10, cAppend);
  const s3Cell = progress(frame, cAppend, 15);
  const committed3 = frame >= cCommit + 10;
  const applied = frame >= cApply + 24;

  const clientIn = progress(frame, cClient, 15);
  const clientOp = clientIn * anyFocus(focusOpacity(frame, cClient, cAE), focusOpacity(frame, cCommit, cApply));
  const reqT = linear(frame, cClient + 8, 24);
  const okT = linear(frame, cCommit + 12, 24);

  const toS2 = fan("S3", "S2", 3, 100);
  const toS4 = fan("S3", "S4", 3, 100);
  // S5's message bends down to the S5 row and stalls there, so the slow follower is clearly S5.
  const s5Start = fan("S3", "S5", 3, 0);
  const toS5 = { ...s5Start, cx: s5Start.x1 + 200, cy: rowMid("S5") };
  const aeP = progress(frame, cAE, 24);
  const s5P = 0.8 * progress(frame, cAE, 18);
  const aeOp = anyFocus(focusOpacity(frame, cAE, cAck), focusOpacity(frame, cApply));
  const arrived = frame >= cAE + 24;
  const [sx, sy] = alongCurve(toS5.x1, toS5.y1, toS5.cx, toS5.cy, toS5.x2, toS5.y2, s5P);

  const counterOp = progress(frame, cAck, 15) * focusOpacity(frame, cAck, cCommit);
  const hop = markerSlide(frame, cCommit, 2);
  const markerIndex = hop.index;
  const markerOp = anyFocus(base, focusOpacity(frame, cCommit, cApply)) * hop.opacity;
  const hb = linear(frame, cApply, 24);
  const lcOp = progress(frame, cApply + 10, 15);

  const followerCell: CellSpec[] =
    arrived
      ? [{ i: 3, term: 2, cmd: "x←3", state: applied ? "committed" : "pending", check: frame >= cAck, glow: (frame >= cAck && frame < cCommit) || frame >= cApply }]
      : [];

  return (
    <>
      <Diagram>
        <Ruler opacity={base} highlight={frame >= cAppend ? 3 : undefined} />
        <CommitMarker index={markerIndex} opacity={markerOp} glow={frame >= cCommit && frame < cApply} />

        <Node s="S1" role="crashed" opacity={base} />
        <Row s="S1" cells={BASE.map((c) => ({ ...c, opacity: 0.5 * base }))} />

        <Node s="S2" role="follower" opacity={s24} />
        <Row s="S2" cells={BASE.map((c) => ({ ...c, opacity: base }))} />
        {frame >= cAE && !arrived ? <Slot s="S2" i={3} opacity={aeOp} /> : null}
        <G opacity={s24}>
          <Row s="S2" cells={followerCell} />
        </G>

        <Node s="S3" role="leader" />
        <G opacity={s3Tag}>
          <Badge x={LOG_LABEL_X} y={(LOG_ROW_Y.S2 + LOG_CELL_H + LOG_ROW_Y.S3) / 2 - 2} text="term 2" size={20} color={t.canvas} stroke={t.c3} />
        </G>
        <Row s="S3" cells={BASE.map((c) => ({ ...c, opacity: s3Base, check: true }))} />
        <Row
          s="S3"
          cells={[
            {
              i: 3,
              term: 2,
              cmd: "x←3",
              state: committed3 ? "committed" : "pending",
              opacity: s3Cell * anyFocus(focusOpacity(frame, cAppend, cAck), focusOpacity(frame, cCommit)),
              dy: (1 - s3Cell) * 24,
              glow: frame >= cAppend && frame < cAE,
              check: committed3,
            },
          ]}
        />

        <Node s="S4" role="follower" opacity={s24} />
        <Row s="S4" cells={BASE.map((c) => ({ ...c, opacity: base }))} />
        {frame >= cAE && !arrived ? <Slot s="S4" i={3} opacity={aeOp} /> : null}
        <G opacity={s24}>
          <Row s="S4" cells={followerCell} />
        </G>

        <Node s="S5" role="follower" opacity={s5} />
        <Row s="S5" cells={BASE.map((c) => ({ ...c, opacity: base }))} />
        {frame >= cAE ? <Slot s="S5" i={3} opacity={rowsAE} /> : null}

        {frame >= cAE ? (
          <G opacity={aeOp} glow={frame < cAck}>
            <CurvedArrow {...toS2} progress={aeP} color={t.heading} width={3} />
            <CurvedArrow {...toS4} progress={aeP} color={t.heading} width={3} />
            <G opacity={frame < cApply ? 1 : 0}>
              <CurvedArrow {...toS5} progress={s5P} color={t.heading} width={3} />
              {s5P > 0.05 ? <circle cx={sx} cy={sy} r={12} fill={t.heading} /> : null}
              <Label x={sx + 26} y={sy + 9} size={26} anchor="start" color={t.heading} opacity={progress(frame, cAE + 10, 8)}>
                ponawia ↻
              </Label>
            </G>
            <Message {...toS2} t={linear(frame, cAE, 24)} />
            <Message {...toS4} t={linear(frame, cAE, 24)} />
            <Message {...toS2} t={hb} color={t.success} />
            <Message {...toS4} t={hb} color={t.success} />
          </G>
        ) : null}

        {frame >= cApply ? (
          <G opacity={lcOp} glow>
            <Badge x={toS4.x1 + 250} y={toS4.cy + 4} text="leaderCommit=3" color={t.successSoft} stroke={t.success} size={26} />
          </G>
        ) : null}

        {frame >= cClient ? (
          <G opacity={clientOp} glow={frame < cAppend || (frame >= cCommit && frame < cApply)}>
            <rect x={1460} y={rowMid("S3") - 36} width={240} height={72} rx={36} fill={t.inset} stroke={t.muted} strokeWidth={3} />
            <Label x={1580} y={rowMid("S3") + 10} size={30} weight={700}>
              klient
            </Label>
            {reqT > 0 && reqT < 1 ? (
              <Badge x={1400 - (1400 - 900) * reqT} y={rowMid("S3")} text="x←3" color={t.surface} stroke={t.heading} size={26} />
            ) : null}
            {okT > 0 ? (
              <G opacity={progress(frame, cCommit + 12, 8)}>
                <Badge x={900 + (1380 - 900) * okT} y={rowMid("S3")} text="OK" color={t.successSoft} stroke={t.success} size={26} />
              </G>
            ) : null}
          </G>
        ) : null}
      </Diagram>

      <Fade opacity={counterOp} dy={(1 - progress(frame, cAck, 15)) * 24}>
        <Card x={1400} y={260} w={360} h={200} glow={frame >= cAck && frame < cCommit}>
          <Text size={96} weight={700} mono color={t.heading} style={{ lineHeight: 1 }}>
            3/5
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 12 }}>
            większość
          </Text>
        </Card>
      </Fade>
    </>
  );
};

const FULL_3: CellSpec = { i: 3, term: 2, cmd: "x←3", state: "committed" };
const FULL_4: CellSpec = { i: 4, term: 2, cmd: "y←7", state: "committed" };

const ConsistencyCheck: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cNew = cue("new_entry");
  const cFields = cue("message_fields");
  const cCheck = cue("follower_check");
  const cOk = cue("match_ok");
  const cRule = cue("log_matching");

  const base = dimFrom(frame, cNew);
  const newIn = progress(frame, cNew, 15);
  const toS2 = fan("S3", "S2", 4, 100);
  const toS4 = fan("S3", "S4", 4, 100);
  const msgOp = focusOpacity(frame, cFields, cRule) * (1 - progress(frame, cRule, 10));
  const cardIn = progress(frame, cFields, 15);
  const cardOp = cardIn * focusOpacity(frame, cFields, cRule);
  const compareIn = progress(frame, cCheck, 15);
  const compareOp = compareIn * focusOpacity(frame, cCheck, cRule);
  const okIn = progress(frame, cOk, 15);
  const appended = frame >= cOk + 10;
  const hop = markerSlide(frame, cOk, 3);
  const markerIndex = hop.index;
  const markerOp = anyFocus(base, focusOpacity(frame, cOk, cRule)) * hop.opacity;
  const ruleIn = progress(frame, cRule, 15);
  const s2Op = anyFocus(focusOpacity(frame, cFields, cRule), base * (frame < cNew ? 1 : 0), progress(frame, cRule, 10));
  const s4Op = anyFocus(focusOpacity(frame, cOk, cRule), base * (frame < cNew ? 1 : 0), progress(frame, cRule, 10));
  const ruleRows = anyFocus(base, progress(frame, cRule, 10));

  const s3State: CellState = appended ? "committed" : "pending";
  const s3Glow = frame >= cNew && frame < cFields;

  return (
    <>
      <Diagram>
        <Ruler opacity={base} highlight={frame >= cCheck && frame < cOk ? 3 : frame >= cNew && frame < cRule ? 4 : undefined} />
        <CommitMarker index={markerIndex} opacity={markerOp} glow={frame >= cOk && frame < cRule} />

        <Node s="S1" role="crashed" opacity={base} />
        <Row s="S1" cells={BASE.map((c) => ({ ...c, opacity: 0.5 * base }))} />

        <Node s="S2" role="follower" opacity={s2Op} />
        <Row
          s="S2"
          cells={[...BASE, FULL_3].map((c) => ({
            ...c,
            opacity: c.i === 3 ? anyFocus(ruleRows, focusOpacity(frame, cCheck, cOk)) : ruleRows,
            glow: c.i === 3 && frame >= cCheck && frame < cOk,
          }))}
        />
        {frame >= cFields && !appended ? <Slot s="S2" i={4} opacity={msgOp} /> : null}

        <Node s="S3" role="leader" />
        <Row s="S3" cells={[...BASE, FULL_3].map((c) => ({ ...c, opacity: ruleRows }))} />
        <Row
          s="S3"
          cells={[
            {
              ...FULL_4,
              state: s3State,
              opacity: newIn * anyFocus(focusOpacity(frame, cNew, cCheck), focusOpacity(frame, cOk)),
              dy: (1 - newIn) * 24,
              glow: s3Glow,
            },
          ]}
        />

        <Node s="S4" role="follower" opacity={s4Op} />
        <Row s="S4" cells={[...BASE, FULL_3].map((c) => ({ ...c, opacity: ruleRows }))} />
        {frame >= cOk && !appended ? <Slot s="S4" i={4} opacity={s4Op} /> : null}

        <Node s="S5" role="follower" opacity={base} />
        <Row s="S5" cells={BASE.map((c) => ({ ...c, opacity: base }))} />

        {appended ? (
          <G opacity={okIn * (1 - progress(frame, cRule, 10))} glow={frame < cRule}>
            <Row s="S2" cells={[{ ...FULL_4, check: true }]} />
            <Row s="S4" cells={[{ ...FULL_4, check: true }]} />
          </G>
        ) : null}
        {appended && frame >= cRule ? (
          <>
            <Row s="S2" cells={[FULL_4]} />
            <Row s="S4" cells={[FULL_4]} />
          </>
        ) : null}

        {frame >= cFields ? (
          <G opacity={msgOp} glow={frame < cCheck}>
            <CurvedArrow {...toS2} progress={progress(frame, cFields, 24)} color={t.heading} width={3} />
            <Message {...toS2} t={linear(frame, cFields, 24)} />
          </G>
        ) : null}
        {frame >= cOk ? (
          <G opacity={1 - progress(frame, cRule, 10)}>
            <CurvedArrow {...toS4} progress={progress(frame, cOk, 10)} color={t.heading} width={3} />
          </G>
        ) : null}

        {frame >= cCheck ? (
          <G opacity={compareOp} glow={frame < cOk}>
            <Badge x={PANEL_X + 250} y={612} text="term 2 = term 2" color={t.surface} stroke={t.heading} size={30} />
            {frame >= cOk ? <Check x={PANEL_X + 450} y={612} s={24} /> : null}
          </G>
        ) : null}

        {/* Right edge padded past the commit line, so the line runs inside the hull instead of cutting its border; glow stays on the rule card. */}
        {frame >= cRule ? (
          <Hull x={logCellX(1) - 12} y={LOG_ROW_Y.S2 - 12} w={cellRight(4) + 24 - (logCellX(1) - 12)} h={LOG_ROW_Y.S4 + LOG_CELL_H - LOG_ROW_Y.S2 + 24} opacity={ruleIn} glow={false} />
        ) : null}
      </Diagram>

      <Fade opacity={cardOp} dy={(1 - cardIn) * 24}>
        <Card x={PANEL_X} y={290} w={PANEL_W} h={260} glow={frame >= cFields && frame < cCheck}>
          <Fields
            title="AppendEntries → S2"
            lines={["prevLogIndex=3", "prevLogTerm=2", "entries=[y←7]"]}
            hot={frame >= cCheck && frame < cRule ? [0, 1] : []}
          />
        </Card>
      </Fade>

      <Fade opacity={ruleIn} dy={(1 - ruleIn) * 24}>
        <Card x={PANEL_X} y={680} w={PANEL_W} h={220} glow>
          <Text size={36} weight={700} mono color={t.heading}>
            Log Matching
          </Text>
          <Text size={30} style={{ marginTop: 14 }}>
            Ten sam index i term → identyczne logi do tego miejsca
          </Text>
        </Card>
      </Fade>
    </>
  );
};

const LogRepair: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cBack = cue("s1_returns");
  const cNext = cue("next_index_init");
  const cRej4 = cue("reject_4");
  const cRej3 = cue("reject_3");
  const cMatch = cue("match_2");
  const cOver = cue("overwrite_tail");

  const others = dimFrom(frame, cBack);
  const back = progress(frame, cBack, 10);
  const s1Role: Role = frame >= cBack + 5 ? "follower" : "crashed";
  const s1Base = 0.5 + 0.5 * back;
  const zIn = progress(frame, cBack + 10, 15);
  const nextIn = progress(frame, cNext, 15);
  const nextOp = nextIn * (1 - progress(frame, cOver, 12)) * focusOpacity(frame, cNext, cMatch);
  const msg = fanLeft();
  const msgOp = progress(frame, cNext, 10) * anyFocus(focusOpacity(frame, cNext, cRej4), focusOpacity(frame, cMatch, cOver + 40));
  const cardIn = progress(frame, cNext, 15);
  const cardOp = cardIn * anyFocus(focusOpacity(frame, cNext, cRej4), focusOpacity(frame, cMatch, cOver));
  const noteOp = 0.5 * progress(frame, cRej4, 12) * (1 - progress(frame, cMatch, 12));
  const note2 = progress(frame, cRej3, 12);
  const matched = frame >= cMatch;
  const zState: CellState = frame >= cOver ? "conflict" : "pending";
  const zOp = zIn * (1 - progress(frame, cOver + 20, 15));
  const slide3 = progress(frame, cOver + 35, 18);
  const slide4 = progress(frame, cOver + 47, 18);
  const finalOp = progress(frame, cOver + 65, 15);
  const s1Row = anyFocus(focusOpacity(frame, cBack, cNext), focusOpacity(frame, cMatch));
  const leaderNote = progress(frame, cOver + 75, 15);

  return (
    <>
      <Diagram>
        <Ruler opacity={others} highlight={frame >= cNext && frame < cMatch ? 3 : frame >= cMatch && frame < cOver ? 2 : undefined} />
        <CommitMarker index={4} opacity={others} />

        <Node s="S1" role={s1Role} />
        <Row
          s="S1"
          cells={BASE.map((c) => ({
            ...c,
            opacity: s1Base * (frame < cBack ? 1 : anyFocus(s1Row, c.i === 2 ? focusOpacity(frame, cMatch, cOver) : 0)),
            glow: c.i === 2 && matched && frame < cOver,
          }))}
        />
        {zIn > 0 ? (
          <Row
            s="S1"
            cells={[{ i: 3, term: 1, cmd: "z←0", state: zState, opacity: zOp * anyFocus(s1Row, focusOpacity(frame, cNext, cMatch)), dy: (1 - zIn) * 24, glow: frame >= cBack && frame < cNext }]}
          />
        ) : null}
        {slide3 > 0 ? (
          <G glow={finalOp > 0}>
            <Row s="S1" cells={[{ ...FULL_3, opacity: slide3, dx: (1 - slide3) * 80 }]} />
            <Row s="S1" cells={[{ ...FULL_4, opacity: slide4, dx: (1 - slide4) * 80 }]} />
          </G>
        ) : null}

        {frame >= cNext ? (
          <G opacity={nextOp} glow={frame < cRej4}>
            <rect x={logCellX(3) - 8} y={LOG_ROW_Y.S1 - 8} width={LOG_CELL_W + 16} height={LOG_CELL_H + 16} rx={16} fill="none" stroke={t.heading} strokeWidth={4} />
            <line x1={cellRight(4) + 20} y1={rowMid("S1")} x2={cellRight(3) + 14} y2={rowMid("S1")} stroke={t.heading} strokeWidth={4} strokeLinecap="round" />
            <polygon
              points={`${cellRight(3) + 12},${rowMid("S1")} ${cellRight(3) + 30},${rowMid("S1") - 10} ${cellRight(3) + 30},${rowMid("S1") + 10}`}
              fill={t.heading}
            />
            <Badge x={cellRight(4) + 122} y={rowMid("S1")} text="nextIndex=3" stroke={t.heading} size={24} />
          </G>
        ) : null}

        <Node s="S2" role="follower" opacity={others} />
        <Row s="S2" cells={[...BASE, FULL_3, FULL_4].map((c) => ({ ...c, opacity: others }))} />
        <Node s="S3" role="leader" />
        <Row
          s="S3"
          cells={[...BASE, FULL_3, FULL_4].map((c) => ({
            ...c,
            opacity: anyFocus(others, c.i === 2 ? focusOpacity(frame, cMatch, cOver) : 0, c.i >= 3 ? focusOpacity(frame, cOver, cOver + 65) : 0),
            glow: c.i === 2 && matched && frame < cOver,
          }))}
        />
        <Node s="S4" role="follower" opacity={others} />
        <Row s="S4" cells={[...BASE, FULL_3, FULL_4].map((c) => ({ ...c, opacity: others }))} />
        <Node s="S5" role="follower" opacity={others} />
        <Row s="S5" cells={BASE.map((c) => ({ ...c, opacity: others }))} />

        {frame >= cNext ? (
          <G opacity={msgOp}>
            <CurvedArrow {...msg} progress={progress(frame, cNext, 24)} color={t.heading} width={3} />
            <Message {...msg} t={linear(frame, cNext, 24)} />
            <Message {...msg} t={linear(frame, cMatch - 20, 20)} />
            <Message {...msg} t={linear(frame, cOver, 20)} />
          </G>
        ) : null}

        {finalOp > 0 ? <Hull x={logCellX(1) - 12} y={LOG_ROW_Y.S1 - 12} w={cellRight(4) - logCellX(1) + 24} h={LOG_CELL_H + 24} opacity={finalOp} /> : null}
      </Diagram>

      <Fade opacity={cardOp} dy={(1 - cardIn) * 24}>
        <Card x={PANEL_X} y={290} w={PANEL_W} h={260} glow={(frame >= cNext && frame < cRej4) || (matched && frame < cOver)}>
          <Fields
            title="AppendEntries → S1"
            lines={["prevLogIndex=2", "prevLogTerm=1", "entries=[x←3, y←7]"]}
            hot={matched && frame < cOver ? [0, 1] : []}
          />
        </Card>
      </Fade>

      {/* Drawn after the card so the card background does not hide it. */}
      {matched ? (
        <Diagram>
          <G opacity={progress(frame, cMatch, 12) * (1 - progress(frame, cOver, 12))} glow={frame < cOver}>
            <Check x={PANEL_X + PANEL_W - 52} y={340} s={26} />
          </G>
        </Diagram>
      ) : null}

      <Fade opacity={noteOp}>
        <div style={{ position: "absolute", left: PANEL_X, top: 600, width: PANEL_W }}>
          <Text size={30} color={t.muted}>
            gdyby się nie zgadzało: odmowa <span style={{ color: t.danger }}>✕</span>
          </Text>
          <Text size={30} color={t.muted} style={{ marginTop: 12, opacity: note2 }}>
            → nextIndex − 1 i ponowienie
          </Text>
        </div>
      </Fade>

      <Fade opacity={leaderNote} dy={(1 - leaderNote) * 24}>
        <div style={{ position: "absolute", left: PANEL_X, top: 610, width: PANEL_W }}>
          <Text size={32} weight={600}>
            leader nigdy nie nadpisuje
            <br />
            własnego logu
          </Text>
        </div>
      </Fade>
    </>
  );
};

// AppendEntries to S1 travels along the left of the row labels, clear of every log row.
const fanLeft = () => {
  const r = 38;
  const x = LOG_LABEL_X - r + 4;
  return { x1: x, y1: rowMid("S3") - 20, cx: 110, cy: rowMid("S2"), x2: x, y2: rowMid("S1") + 20 };
};

export const scenes: Record<string, FC> = {
  log_append: LogAppend,
  consistency_check: ConsistencyCheck,
  log_repair: LogRepair,
};
