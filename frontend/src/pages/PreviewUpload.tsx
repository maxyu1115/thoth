import { FormGroup, FormControlLabel, Checkbox, Button } from '@mui/material';
import { CustomDropzone, VideoPlayer } from '../components';
import { useRef, useState } from 'react';
import { VideoJsPlayer } from 'video.js';
import { DropEvent } from 'react-dropzone';
import { uploadVideo } from '../dataloader';

export const PreviewUpload = ({
  onUploadFinish,
}: {
  onUploadFinish?: (data: string) => void;
}): JSX.Element => {
  const [isAnimated, setIsAnimated] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');

  const playerRef = useRef<VideoJsPlayer | null>(null);

  const handlePlayerReady = (player: VideoJsPlayer): void => {
    playerRef.current = player;
  };

  const handleDropAccepted = <T extends File>(
    files: T[],
    event: DropEvent,
  ): void => {
    event.preventDefault();

    uploadVideo(files?.[0], isAnimated)
      .then((response) => {
        console.log(response.data);
        onUploadFinish?.(files?.[0].name);
      })
      .catch((err) => console.log(err));

    setVideoUrl(URL.createObjectURL(files?.[0]));
  };

  return videoUrl === '' ? (
    <>
      <FormGroup>
        <FormControlLabel
          control={
            <Checkbox
              checked={isAnimated}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setIsAnimated(e.target.checked)
              }
            />
          }
          label="Does this video have animated slides?"
        />
      </FormGroup>
      <CustomDropzone onDropAccepted={handleDropAccepted} />
    </>
  ) : (
    <>
      <VideoPlayer
        onReady={handlePlayerReady}
        options={{
          fluid: true,
          controls: true,
          sources: [{ src: videoUrl, type: 'video/mp4' }],
        }}
      />
      <Button
        onClick={() => playerRef.current?.currentTime(87)}
        variant="contained"
      >
        Skip
      </Button>
    </>
  );
};
