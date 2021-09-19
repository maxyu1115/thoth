import { useEffect, useRef } from 'react';

import videojs, { VideoJsPlayer, VideoJsPlayerOptions } from 'video.js';
import 'video.js/dist/video-js.css';

export const VideoPlayer = ({
  onReady,
  options,
  curTime,
}: {
  onReady?: (player: VideoJsPlayer) => void;
  options?: VideoJsPlayerOptions;
  curTime?: number;
}): JSX.Element => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const playerRef = useRef<VideoJsPlayer | null>(null);

  useEffect(() => {
    if (playerRef.current == null) {
      const videoElement = videoRef.current;

      if (videoElement == null) return;

      const player = (playerRef.current = videojs(videoElement, options, () => {
        console.log('Player is ready!');
        player.currentTime(curTime ?? 0);
      }));
    }
  }, [options]);

  useEffect(
    () => () => {
      if (playerRef.current != null) {
        playerRef.current.dispose();
        playerRef.current = null;
      }
    },
    [],
  );

  return (
    <div>
      <video
        ref={videoRef}
        className="video-js vjs-big-play-centered vjs-fluid"
      />
    </div>
  );
};
