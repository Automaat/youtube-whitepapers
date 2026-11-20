import type { FC, ReactNode } from "react";
import {
  Badge,
  Card,
  Check,
  Cross,
  DIM,
  Diagram,
  G,
  Label,
  LogCell,
  Message,
  RoleNode,
  Serif,
  Text,
  enter,
  linear,
  progress,
  useScene,
  useTheme,
  type CellState,
  type Role,
} from "../../design";
import { LOG_CELL_H, LOG_CELL_W, LOG_LABEL_X, LOG_ROW_Y, LOG_RULER_Y, SERVERS, logCellX, type Server } from "./layout";

const colX = (i: number) => logCellX(i) + LOG_CELL_W / 2;
const rowMid = (s: Server) => LOG_ROW_Y[s] + LOG_CELL_H / 2;
const GRID_BOTTOM = LOG_ROW_Y.S5 + LOG_CELL_H;
const VOTE_COL = 5;
const PANEL_X = 1240;
const PANEL_W = 560;

const active = (frame: number, ...wins: [number, number][]) =>
  DIM + (1 - DIM) * Math.max(0, ...wins.map(([a, b]) => progress(frame, a, 10) - (b === Infinity ? 0 : progress(frame, b, 10))));

const fade = (frame: number, at: number, until = Infinity) =>
  progress(frame, at, 12) * (until === Infinity ? 1 : 1 - progress(frame, until, 12));

const Cell = ({ s, i, term, cmd, state = "pending" }: { s: Server; i: number; term?: number; cmd?: string; state?: CellState }) => (
  <LogCell x={logCellX(i)} y={LOG_ROW_Y[s]} w={LOG_CELL_W} h={LOG_CELL_H} term={term} cmd={cmd} state={state} />
);

const Slot = ({ s, i }: { s: Server; i: number }) => <Cell s={s} i={i} state="empty" />;

const RowNode = ({ s, role }: { s: Server; role: Role }) => (
  <RoleNode x={LOG_LABEL_X} y={rowMid(s)} label={s} role={role} r={38} fontSize={24} />
);

const Ruler = ({ n, vote = 0, voteCol = VOTE_COL, voteX, label = false }: { n: number; vote?: number; voteCol?: number; voteX?: number; label?: boolean }) => {
  const t = useTheme();
  return (
    <g>
      {label ? (
        <Label x={LOG_LABEL_X} y={LOG_RULER_Y + 12} size={24} color={t.muted} mono>
          index
        </Label>
      ) : null}
      {Array.from({ length: n }, (_, k) => (
        <Label key={k} x={colX(k + 1)} y={LOG_RULER_Y + 8} size={24} mono color={t.muted}>
          {k + 1}
        </Label>
      ))}
      {vote > 0 ? (
        <Label x={voteX ?? colX(voteCol)} y={LOG_RULER_Y + 8} size={24} color={t.muted} opacity={vote}>
          głos
        </Label>
      ) : null}
    </g>
  );
};

const CommitLine = ({ after, opacity = 1 }: { after: number; opacity?: number }) => {
  const t = useTheme();
  const x = logCellX(after) + LOG_CELL_W + 9;
  return (
    <g opacity={opacity}>
      <line x1={x} y1={LOG_RULER_Y + 18} x2={x} y2={GRID_BOTTOM + 10} stroke={t.success} strokeWidth={5} strokeLinecap="round" />
      <Label x={x} y={GRID_BOTTOM + 46} size={24} mono color={t.success}>
        commit
      </Label>
    </g>
  );
};

const Highlight = ({ x, y, w, h }: { x: number; y: number; w: number; h: number }) => {
  const t = useTheme();
  return <rect x={x - 5} y={y - 5} width={w + 10} height={h + 10} rx={16} fill="none" stroke={t.heading} strokeWidth={4} />;
};

const cellBox = (s: Server, i: number) => ({ x: logCellX(i), y: LOG_ROW_Y[s], w: LOG_CELL_W, h: LOG_CELL_H });

const VoteMark = ({ s, ok, opacity = 1, col = VOTE_COL, x }: { s: Server; ok: boolean; opacity?: number; col?: number; x?: number }) => {
  const cx = x ?? colX(col);
  return <g opacity={opacity}>{ok ? <Check x={cx} y={rowMid(s)} s={24} /> : <Cross x={cx} y={rowMid(s)} s={24} />}</g>;
};

const Panel = ({
  at,
  until = Infinity,
  x = PANEL_X,
  y,
  w = PANEL_W,
  h,
  glow = false,
  dim = 1,
  danger = false,
  children,
}: {
  at: number;
  until?: number;
  x?: number;
  y: number;
  w?: number;
  h: number;
  glow?: boolean;
  dim?: number;
  danger?: boolean;
  children: ReactNode;
}) => {
  const { frame } = useScene();
  const t = useTheme();
  const e = enter(frame, at);
  const out = until === Infinity ? 1 : 1 - progress(frame, until, 12);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, transform: e.transform, opacity: e.opacity * out * dim }}>
      <Card x={x} y={y} w={w} h={h} glow={glow} style={danger ? { border: `2px solid ${t.danger}` } : undefined}>
        {children}
      </Card>
    </div>
  );
};

const Ok = () => {
  const t = useTheme();
  return <span style={{ color: t.success, marginRight: 10 }}>✓</span>;
};

const No = () => {
  const t = useTheme();
  return <span style={{ color: t.danger, marginRight: 10 }}>✕</span>;
};

const StepCard = ({ steps }: { steps: { at: number; tag: string; caption: string }[] }) => {
  const { frame } = useScene();
  const t = useTheme();
  const cur = [...steps].reverse().find((s) => frame >= s.at);
  if (!cur) return null;
  const e = enter(frame, cur.at);
  return (
    <Panel at={steps[0].at} y={170} h={150}>
      <div style={{ display: "flex", alignItems: "center", gap: 28, height: "100%", ...e }}>
        <Serif size={84}>{cur.tag}</Serif>
        <Text size={32} weight={700} color={t.ink}>
          {cur.caption}
        </Text>
      </div>
    </Panel>
  );
};

/* ------------------------------------------------------------ election_restriction */

// Same 5-column index ruler as the other log-grid scenes; the vote column sits after index 5.
const ER_VOTE_X = logCellX(5) + LOG_CELL_W + 50;
const ER_PANEL_X = 1290;
const ER_PANEL_W = 520;

const ElectionRestriction: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const cCand = cue("s1_candidate");
  const cReq = cue("vote_request_fields");
  const cCmp = cue("compare_last_term");
  const cDen = cue("votes_denied");
  const cOv = cue("overlap");

  const rowOp: Record<Server, number> = {
    S1: active(frame, [-10, cOv]),
    S2: active(frame, [-10, cCand], [cCmp, Infinity]),
    S3: active(frame, [-10, cCand], [cOv, Infinity]),
    S4: active(frame, [-10, cCand], [cDen, Infinity]),
    S5: active(frame, [-10, cCand], [cDen, Infinity]),
  };
  const full = (s: Server) => s === "S2" || s === "S3" || s === "S4";
  // Votes stay readable (dimmed) during the overlap, so the hulls are not mistaken for the actual votes.
  const votesOp = progress(frame, cCand, 12) * (1 - (1 - DIM) * progress(frame, cOv, 10));
  const cmpOp = fade(frame, cCmp, cDen);
  const hullP = progress(frame, cOv, 18);
  const lineOp = 1 - progress(frame, cOv, 10);

  const hullA = { x: 176, y: LOG_ROW_Y.S2 - 14, x2: 1016, y2: LOG_ROW_Y.S4 + LOG_CELL_H + 14 };
  const hullB = { x: 160, y: LOG_ROW_Y.S3 - 14, x2: 1172, y2: LOG_ROW_Y.S5 + LOG_CELL_H + 14 };

  return (
    <>
      <Diagram>
        <g style={enter(frame, 0)}>
          <Ruler n={5} vote={votesOp} voteX={ER_VOTE_X} label />
          {SERVERS.map((s) => (
            <G key={s} opacity={rowOp[s]}>
              <G glow={s === "S1" && frame >= cCand && frame < cReq}>
                <RowNode s={s} role={s === "S1" && frame >= cCand ? "candidate" : s === "S3" ? "leader" : "follower"} />
              </G>
              <Cell s={s} i={1} term={1} cmd="x←1" state="committed" />
              <Cell s={s} i={2} term={1} cmd="y←2" state="committed" />
              {full(s) ? <Cell s={s} i={3} term={2} cmd="x←3" state="committed" /> : s === "S1" ? <Cell s={s} i={3} term={1} cmd="z←0" /> : <Slot s={s} i={3} />}
              {full(s) ? <Cell s={s} i={4} term={2} cmd="y←7" state="committed" /> : <Slot s={s} i={4} />}
            </G>
          ))}
          <CommitLine after={4} opacity={lineOp} />
        </g>

        {frame >= cReq && frame < cDen ? (
          <G glow opacity={progress(frame, cReq, 10)}>
            <Highlight {...cellBox("S1", 3)} />
            {frame >= cCmp ? <Highlight {...cellBox("S2", 4)} /> : null}
          </G>
        ) : null}

        <G opacity={cmpOp}>
          <Badge x={ER_VOTE_X} y={rowMid("S2")} text="2 > 1" size={28} stroke={t.heading} />
        </G>

        <g opacity={votesOp}>
          <VoteMark s="S1" ok opacity={frame < cOv ? rowOp.S1 : 1} x={ER_VOTE_X} />
          <VoteMark s="S2" ok={false} opacity={fade(frame, cDen)} x={ER_VOTE_X} />
          <Label x={ER_VOTE_X} y={rowMid("S3") + 12} size={36} weight={700} color={t.muted} opacity={fade(frame, cDen)}>
            –
          </Label>
          <VoteMark s="S4" ok={false} opacity={fade(frame, cDen)} x={ER_VOTE_X} />
          <VoteMark s="S5" ok opacity={fade(frame, cDen)} x={ER_VOTE_X} />
        </g>

        {hullP > 0 ? (
          <g opacity={hullP}>
            <G glow>
              <rect x={hullA.x} y={hullB.y} width={hullA.x2 - hullA.x} height={hullA.y2 - hullB.y} rx={20} fill={t.heading} opacity={0.07} />
            </G>
            <rect x={hullA.x} y={hullA.y} width={hullA.x2 - hullA.x} height={hullA.y2 - hullA.y} rx={20} fill="none" stroke={t.heading} strokeWidth={4} />
            <rect x={hullB.x} y={hullB.y} width={hullB.x2 - hullB.x} height={hullB.y2 - hullB.y} rx={22} fill="none" stroke={t.ink} strokeWidth={4} strokeDasharray="14 10" />
            <Label x={hullA.x2 + 12} y={rowMid("S2") + 9} size={26} anchor="start" color={t.heading}>
              kopie 3–4
            </Label>
            <Label x={hullB.x2} y={hullB.y2 + 42} size={28} anchor="end" color={t.ink}>
              dowolna większość (3 z 5)
            </Label>
          </g>
        ) : null}
      </Diagram>

      <Panel at={cCand} x={ER_PANEL_X} w={ER_PANEL_W} y={290} h={250} glow={frame >= cReq && frame < cCmp} dim={active(frame, [cCand, cCmp])}>
        <Text size={34} weight={700} mono color={t.candidate}>
          S1 · term 3
        </Text>
        <div style={enter(frame, cReq)}>
          <Text size={28} color={t.muted} style={{ marginTop: 12 }}>
            RequestVote
          </Text>
          <Text size={32} weight={700} mono>
            lastLogIndex=3
          </Text>
          <Text size={32} weight={700} mono>
            lastLogTerm=1
          </Text>
        </div>
      </Panel>

      <Panel at={cDen} until={cOv} x={ER_PANEL_X} w={ER_PANEL_W} y={590} h={190} glow>
        <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
          <Serif size={96}>2/5</Serif>
          <Text size={34} weight={700}>
            <No /> za mało głosów
          </Text>
        </div>
      </Panel>

      <Panel at={cOv} x={ER_PANEL_X} w={ER_PANEL_W} y={600} h={170} glow>
        <Text size={34} weight={700}>
          każde dwie większości się przecinają
        </Text>
      </Panel>
    </>
  );
};

/* ------------------------------------------------------------ fig8 shared */

const Repl = ({ from, to, i, at, color }: { from: Server; to: Server; i: number; at: number; color?: string }) => {
  const { frame } = useScene();
  return <Message x1={colX(i)} y1={rowMid(from)} x2={colX(i)} y2={rowMid(to)} t={linear(frame, at, 24)} color={color} />;
};

/* ------------------------------------------------------------ fig8_trap */

const Fig8Trap: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const a = cue("step_a");
  const b = cue("step_b");
  const c = cue("step_c");
  const m = cue("majority_not_commit");
  const d = cue("step_d");
  const ow = cue("overwrite");
  // Step (b) reads as: candidate → 3 votes → leader → writes term-3 entry, all early in the cue.
  const bLead = b + 30;

  const roleS1: Role = frame >= d ? "crashed" : frame >= c ? "leader" : frame >= b ? "crashed" : frame >= a ? "leader" : "follower";
  const roleS5: Role =
    frame >= d + 30 ? "leader" : frame >= d ? "candidate" : frame >= c ? "crashed" : frame >= bLead ? "leader" : frame >= b ? "candidate" : "follower";
  const role = (s: Server): Role => (s === "S1" ? roleS1 : s === "S5" ? roleS5 : "follower");

  const rowOp: Record<Server, number> = {
    S1: active(frame, [-10, a], [a, b], [c, d]),
    S2: active(frame, [-10, a], [a, b], [m, Infinity]),
    S3: active(frame, [-10, a], [b, Infinity]),
    S4: active(frame, [-10, a], [b, c], [d, Infinity]),
    S5: active(frame, [-10, a], [b, c], [d, Infinity]),
  };

  const replaced = frame >= ow + 24;
  const votesB = fade(frame, b + 4, c);
  const votesD = fade(frame, d + 10);
  const glowNode = (s: Server) =>
    (s === "S1" && ((frame >= a && frame < b) || (frame >= c && frame < m))) || (s === "S5" && ((frame >= b && frame < c) || (frame >= d && frame < ow)));

  const idx2 = (s: Server) => {
    if (s === "S1") return frame >= a ? <Cell s={s} i={2} term={2} /> : <Slot s={s} i={2} />;
    if (s === "S2" || s === "S3") {
      const has = s === "S2" ? frame >= a + 24 : frame >= c + 24;
      if (!has) return <Slot s={s} i={2} />;
      if (replaced) return <Cell s={s} i={2} term={3} />;
      if (frame >= ow) return <Cell s={s} i={2} term={2} state="conflict" />;
      return <Cell s={s} i={2} term={2} />;
    }
    if (s === "S4") return replaced ? <Cell s={s} i={2} term={3} /> : <Slot s={s} i={2} />;
    return frame >= bLead + 6 ? <Cell s={s} i={2} term={3} /> : <Slot s={s} i={2} />;
  };

  return (
    <>
      <Diagram>
        <g style={enter(frame, 0)}>
          <Ruler n={3} vote={Math.max(votesB, votesD)} voteCol={4} />
          {SERVERS.map((s) => (
            <G key={s} opacity={rowOp[s]}>
              <G glow={glowNode(s)}>
                <RowNode s={s} role={role(s)} />
              </G>
              <Cell s={s} i={1} term={1} state="committed" />
              {idx2(s)}
              {s === "S1" && frame >= c + 30 ? <Cell s={s} i={3} term={4} /> : <Slot s={s} i={3} />}
            </G>
          ))}
        </g>

        <Repl from="S1" to="S2" i={2} at={a} />
        <Repl from="S1" to="S3" i={2} at={c} />
        {(["S2", "S3", "S4"] as Server[]).map((s) => (
          <Repl key={s} from="S5" to={s} i={2} at={ow} />
        ))}

        <g opacity={votesB}>
          {(["S3", "S4", "S5"] as Server[]).map((s) => (
            <VoteMark key={s} s={s} ok col={4} />
          ))}
        </g>
        <g opacity={votesD}>
          {(["S2", "S3", "S4", "S5"] as Server[]).map((s) => (
            <VoteMark key={s} s={s} ok col={4} />
          ))}
        </g>

        {frame >= m ? (
          <G glow={frame < d} opacity={fade(frame, m, d)}>
            <rect
              x={logCellX(2) - 10}
              y={LOG_ROW_Y.S1 - 10}
              width={LOG_CELL_W + 20}
              height={LOG_ROW_Y.S3 + LOG_CELL_H - LOG_ROW_Y.S1 + 20}
              rx={18}
              fill="none"
              stroke={t.heading}
              strokeWidth={4}
            />
          </G>
        ) : null}

        {frame >= ow ? (
          <G glow opacity={progress(frame, ow, 10)}>
            <Highlight {...cellBox("S2", 2)} />
            <Highlight {...cellBox("S3", 2)} />
          </G>
        ) : null}
      </Diagram>

      <StepCard
        steps={[
          { at: a, tag: "(a)", caption: "S1 leader · term 2" },
          { at: b, tag: "(b)", caption: "S5 kandyduje · term 3" },
          { at: bLead, tag: "(b)", caption: "S5 leader · term 3" },
          { at: c, tag: "(c)", caption: "S1 leader · term 4" },
          { at: d, tag: "(d)", caption: "S5 wygrywa wybory" },
        ]}
      />

      <Panel at={m} y={420} h={200} glow={frame < d} dim={active(frame, [m, d])}>
        <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
          <Serif size={96}>3/5</Serif>
          <div>
            <Text size={34} weight={700}>
              większość,
            </Text>
            <Text size={34} weight={700}>
              <No />
              ale nie commit
            </Text>
          </div>
        </div>
      </Panel>
    </>
  );
};

/* ------------------------------------------------------------ fig8_fix */

const RewindTag = ({ x, y }: { x: number; y: number }) => {
  const t = useTheme();
  return (
    <g>
      <g fill={t.heading}>
        <polygon points={`${x},${y} ${x + 16},${y - 11} ${x + 16},${y + 11}`} />
        <polygon points={`${x + 16},${y} ${x + 32},${y - 11} ${x + 32},${y + 11}`} />
      </g>
      <Label x={x + 48} y={y + 10} size={28} weight={700} anchor="start">
        cofamy
      </Label>
    </g>
  );
};

const Fig8Fix: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const rw = cue("rewind_c");
  const rep = cue("replicate_current");
  const cm = cue("commit_both");
  const blk = cue("s5_blocked");
  const rule = cue("rule_card");
  // Glow hands over from the index-3 commit to the indirect index-2 commit about 1 s later.
  const hand = cm + 30;

  const roleS1: Role = frame >= blk ? "crashed" : "leader";
  const roleS5: Role = frame >= blk ? "candidate" : "crashed";
  const role = (s: Server): Role => (s === "S1" ? roleS1 : s === "S5" ? roleS5 : "follower");
  const committed = frame >= cm;
  const has3 = (s: Server) => s === "S1" || ((s === "S2" || s === "S3") && frame >= rep + 24);

  const rowOp: Record<Server, number> = {
    S1: active(frame, [-10, blk]),
    S2: active(frame, [-10, rule]),
    S3: active(frame, [-10, rule]),
    S4: active(frame, [-10, rep], [blk, rule]),
    S5: active(frame, [-10, rep], [blk, rule]),
  };
  const votes = fade(frame, blk + 10);
  const lineOp = committed ? progress(frame, cm, 12) * (frame >= blk ? 1 - (1 - DIM) * progress(frame, blk, 10) : 1) : 0;

  return (
    <>
      <Diagram>
        <g style={enter(frame, rw)}>
          <Ruler n={3} vote={votes} voteCol={4} />
          {SERVERS.map((s) => {
            const top3 = s === "S1" || s === "S2" || s === "S3";
            return (
              <G key={s} opacity={rowOp[s]}>
                <G glow={(s === "S1" && frame < rep) || (s === "S5" && frame >= blk && frame < rule)}>
                  <RowNode s={s} role={role(s)} />
                </G>
                <Cell s={s} i={1} term={1} state="committed" />
                {top3 ? (
                  <Cell s={s} i={2} term={2} state={committed ? "committed" : "pending"} />
                ) : s === "S5" ? (
                  <Cell s={s} i={2} term={3} />
                ) : (
                  <Slot s={s} i={2} />
                )}
                {has3(s) ? <Cell s={s} i={3} term={4} state={committed ? "committed" : "pending"} /> : <Slot s={s} i={3} />}
              </G>
            );
          })}
        </g>

        <Repl from="S1" to="S2" i={3} at={rep} />
        <Repl from="S1" to="S3" i={3} at={rep} />

        <CommitLine after={3} opacity={lineOp} />

        {frame >= rep && frame < hand ? (
          <G glow opacity={progress(frame, rep, 10)}>
            <rect x={logCellX(3) - 10} y={LOG_ROW_Y.S1 - 10} width={LOG_CELL_W + 20} height={LOG_ROW_Y.S3 + LOG_CELL_H - LOG_ROW_Y.S1 + 20} rx={18} fill="none" stroke={t.heading} strokeWidth={4} />
          </G>
        ) : null}

        {frame >= cm ? (
          <G glow={frame >= hand && frame < blk} opacity={progress(frame, cm, 12) * (frame >= blk ? 1 - (1 - DIM) * progress(frame, blk, 10) : 1)}>
            <rect x={logCellX(2) - 10} y={LOG_ROW_Y.S1 - 10} width={LOG_CELL_W + 20} height={LOG_ROW_Y.S3 + LOG_CELL_H - LOG_ROW_Y.S1 + 20} rx={18} fill="none" stroke={t.success} strokeWidth={4} strokeDasharray="12 8" />
            <Label x={colX(2)} y={GRID_BOTTOM + 46} size={26} color={t.success}>
              pośrednio ✓
            </Label>
          </G>
        ) : null}

        <g opacity={votes}>
          <VoteMark s="S2" ok={false} col={4} />
          <VoteMark s="S3" ok={false} col={4} />
          <VoteMark s="S4" ok col={4} />
          <VoteMark s="S5" ok col={4} />
        </g>
      </Diagram>

      <StepCard
        steps={[
          { at: rw, tag: "(c)", caption: "S1 leader · term 4" },
          { at: rep, tag: "(e)", caption: "kopia wpisu z termu 4" },
        ]}
      />
      <Diagram>
        <G opacity={fade(frame, rw, rep)} glow={frame >= rw && frame < rep}>
          <RewindTag x={PANEL_X + 8} y={140} />
        </G>
      </Diagram>

      <Panel at={cm} y={350} h={150} glow={frame < hand} dim={active(frame, [cm, blk])}>
        <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
          <Serif size={84}>3/5</Serif>
          <Text size={34} weight={700}>
            <Ok /> commit
          </Text>
        </div>
      </Panel>

      <Panel at={blk} y={530} h={150} glow={frame < rule} dim={active(frame, [blk, rule])}>
        <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
          <Serif size={84}>2/5</Serif>
          <Text size={34} weight={700}>
            <No /> S5 przegrywa
          </Text>
        </div>
      </Panel>

      <Panel at={rule} y={710} h={210} glow>
        <Text size={36} weight={700}>
          Liczymy repliki tylko dla wpisów z bieżącego termu
        </Text>
      </Panel>
    </>
  );
};

/* ------------------------------------------------------------ joint_consensus */

const JX: Record<Server, number> = { S1: 300, S2: 520, S3: 740, S4: 1000, S5: 1220 };
const JY = 600;
const OLD = { x: 200, y: 470, x2: 840, y2: 730 };
const NEW = { x: 150, y: 390, x2: 1310, y2: 800 };

const JointConsensus: FC = () => {
  const { frame, cue } = useScene();
  const t = useTheme();
  const grow = cue("grow_cluster");
  const sw = cue("direct_switch");
  const two = cue("two_leaders");
  const je = cue("joint_entry");
  const both = cue("both_majorities");
  const cn = cue("cnew_commit");

  const split = frame >= sw && frame < je;
  const roleOf = (s: Server): Role => {
    if (frame >= je) return s === "S1" ? "leader" : "follower";
    if (frame >= two && (s === "S1" || s === "S5")) return "leader";
    if (frame >= sw && (s === "S1" || s === "S5")) return "candidate";
    return "follower";
  };
  const nodeOp = (s: Server) => (s === "S4" || s === "S5" ? progress(frame, grow, 15) : 1);
  // C_new reaches S1–S3 first; the commit card waits until three chips read C_new.
  const cnAt: Record<Server, number> = { S1: cn, S2: cn + 6, S3: cn + 12, S4: cn + 40, S5: cn + 46 };
  const cnCard = cn + 24;
  const oldOp = progress(frame, grow, 15) * (1 - progress(frame, cnCard + 6, 20));
  const newOp = progress(frame, grow + 10, 15);
  const switchOp = fade(frame, sw, je);
  const rewindOp = fade(frame, je, je + 36);

  return (
    <>
      <Diagram>
        <g opacity={oldOp}>
          <rect x={OLD.x} y={OLD.y} width={OLD.x2 - OLD.x} height={OLD.y2 - OLD.y} rx={40} fill="none" stroke={t.muted} strokeWidth={4} strokeDasharray="16 12" />
          <Label x={OLD.x + 10} y={OLD.y2 + 44} size={30} mono anchor="start" color={t.muted}>
            C_old
          </Label>
        </g>
        <G opacity={newOp}>
          <rect x={NEW.x} y={NEW.y} width={NEW.x2 - NEW.x} height={NEW.y2 - NEW.y} rx={48} fill="none" stroke={t.ink} strokeWidth={4} />
        </G>
        <Label x={NEW.x + 10} y={NEW.y - 20} size={30} mono anchor="start" color={t.ink} opacity={newOp}>
          C_new
        </Label>

        {SERVERS.map((s) => {
          const lead = roleOf(s) === "leader" && frame >= two && frame < je;
          return (
            <G key={s} opacity={nodeOp(s)}>
              <RoleNode x={JX[s]} y={JY} label={s} role={roleOf(s)} r={54} />
              {lead ? (
                <g opacity={progress(frame, two, 12)}>
                  <circle cx={JX[s]} cy={JY} r={68} fill="none" stroke={t.danger} strokeWidth={4} />
                  <Badge x={JX[s]} y={JY + 94} text="term 5" size={24} stroke={t.c3} />
                </g>
              ) : null}
            </G>
          );
        })}
        {/* One conflict mark on a link between the two leaders; a ✕ on each node would read as "crashed". */}
        {frame >= two && frame < je ? (
          <G opacity={progress(frame, two, 12) * (1 - progress(frame, je, 12))} glow>
            <path
              d={`M${JX.S1 + 48} ${JY + 48} Q${(JX.S1 + JX.S5) / 2} ${JY + 290} ${JX.S5 - 48} ${JY + 48}`}
              fill="none"
              stroke={t.danger}
              strokeWidth={4}
              strokeLinecap="round"
            />
            <g opacity={progress(frame, two + 14, 8)}>
              <Cross x={(JX.S1 + JX.S5) / 2} y={JY + 48 + (290 - 48) / 2} s={24} />
            </g>
          </G>
        ) : null}

        <G opacity={rewindOp} glow>
          <g fill={t.heading}>
            <polygon points={`1404,180 1420,169 1420,191`} />
            <polygon points={`1420,180 1436,169 1436,191`} />
          </g>
          <Label x={1452} y={190} size={28} weight={700} anchor="start">
            cofamy
          </Label>
        </G>

        <g opacity={switchOp}>
          {SERVERS.map((s) => (
            <Badge key={s} x={JX[s]} y={JY - 92} text={s === "S1" || s === "S2" ? "C_old" : "C_new"} size={24} />
          ))}
        </g>

        {SERVERS.map((s) => {
          const at1 = je + SERVERS.indexOf(s) * 10;
          const at2 = cnAt[s];
          const second = frame >= at2;
          const op = progress(frame, second ? at2 : at1, 12);
          if (frame < at1) return null;
          return (
            <G key={s} opacity={op} glow={s === "S1" && frame < both}>
              <Badge x={JX[s]} y={JY - 92} text={second ? "C_new" : "C_old,new"} size={22} stroke={t.heading} />
            </G>
          );
        })}
      </Diagram>

      <Panel at={sw} until={je} x={1400} w={424} y={220} h={200} dim={split ? active(frame, [sw, two]) : 1}>
        <Text size={30} weight={700} mono>
          S1 · C_old 2/3 <Ok />
        </Text>
        <Text size={30} weight={700} mono style={{ marginTop: 18 }}>
          S5 · C_new 3/5 <Ok />
        </Text>
      </Panel>

      <Panel at={two} until={je} x={1400} w={424} y={470} h={190} danger glow>
        <Text size={36} weight={700}>
          <No /> dwóch leaderów w jednym termie
        </Text>
      </Panel>

      <Panel at={je} x={1400} w={424} y={220} h={170} glow={frame < both} dim={active(frame, [je, both])}>
        <Text size={28} color={t.muted}>
          joint consensus
        </Text>
        <Text size={36} weight={700} mono style={{ marginTop: 8 }}>
          C_old,new
        </Text>
      </Panel>

      <Panel at={both} x={1400} w={424} y={430} h={200} glow={frame < cn} dim={active(frame, [both, cn])}>
        <Text size={36} weight={700} mono>
          C_old 2/3 <Ok />
        </Text>
        <Text size={36} weight={700} mono style={{ marginTop: 18 }}>
          C_new 3/5 <Ok />
        </Text>
      </Panel>

      <Panel at={cnCard} x={1400} w={424} y={670} h={170} glow>
        <Text size={36} weight={700} mono>
          C_new
        </Text>
        <Text size={30} weight={700} style={{ marginTop: 8 }}>
          commit 3/5 <Ok />
        </Text>
      </Panel>
    </>
  );
};

export const scenes: Record<string, FC> = {
  election_restriction: ElectionRestriction,
  fig8_trap: Fig8Trap,
  fig8_fix: Fig8Fix,
  joint_consensus: JointConsensus,
};
