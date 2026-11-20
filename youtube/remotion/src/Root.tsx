import { Composition, type CalculateMetadataFunction } from "remotion";
import { Episode, Outro, Thumbnail } from "./Episode";
import { FPS, HEIGHT, WIDTH } from "./design/tokens";
import { EMPTY_TIMELINE, type Timeline } from "./timeline";

const fullLength: CalculateMetadataFunction<Timeline> = ({ props }) => ({
  fps: props.fps,
  durationInFrames: Math.max(1, Math.round((props.audioSeconds + props.outroSeconds) * props.fps)),
});

/** Thumbnail spans the episode length so frozen scene frames past frame 0 render. */
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
      calculateMetadata={fullLength}
    />
    <Composition id="Thumbnail" component={Thumbnail} width={WIDTH} height={HEIGHT} fps={FPS} durationInFrames={1} defaultProps={EMPTY_TIMELINE as Timeline} calculateMetadata={fullLength} />
    <Composition id="Outro" component={Outro} width={WIDTH} height={HEIGHT} fps={FPS} durationInFrames={5 * FPS} defaultProps={EMPTY_TIMELINE as Timeline} />
  </>
);
