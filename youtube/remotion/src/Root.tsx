import { Composition, Still } from "remotion";
import { Episode, Outro, Thumbnail } from "./Episode";
import { FPS, HEIGHT, WIDTH } from "./design/tokens";
import { EMPTY_TIMELINE, type Timeline } from "./timeline";

export const Root = () => (
  <>
    <Composition
      id="Episode"
      component={Episode}
      width={WIDTH}
      height={HEIGHT}
      fps={FPS}
      durationInFrames={1}
      defaultProps={EMPTY_TIMELINE as Timeline}
      calculateMetadata={({ props }) => ({
        fps: props.fps,
        durationInFrames: Math.round((props.audioSeconds + props.outroSeconds) * props.fps),
      })}
    />
    <Still id="Thumbnail" component={Thumbnail} width={WIDTH} height={HEIGHT} defaultProps={EMPTY_TIMELINE as Timeline} />
    <Composition id="Outro" component={Outro} width={WIDTH} height={HEIGHT} fps={FPS} durationInFrames={5 * FPS} defaultProps={EMPTY_TIMELINE as Timeline} />
  </>
);
