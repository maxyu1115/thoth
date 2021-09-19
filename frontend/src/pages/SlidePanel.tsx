import { Slides } from '../components';
import { useEffect, useState } from 'react';

import { getSpeechJsonPath } from '../utils';
import { BASE_URL, getFileByPath } from '../dataloader';

interface ImageInfo {
  start_time: number;
  text: string;
  image: string;
  end_time: number;
}

export const SlidePanel = ({
  videoName,
}: {
  videoName: string;
}): JSX.Element => {
  const [speech, setSpeech] = useState<ImageInfo[]>([]);

  useEffect(() => {
    if (videoName !== '') {
      const name = getSpeechJsonPath(videoName);
      getFileByPath(name)
        .then((res) => {
          setSpeech(res.data.splice(1));
        })
        .catch((reason) => console.log(reason));
    }
  }, [videoName]);

  return speech.length === 0 ? (
    <h2>Please upload a video or wait for your upload to complete...</h2>
  ) : (
    <Slides
      slides={speech.map((value, index) => ({
        order: index,
        path: `${BASE_URL}/storage/image/${value.image}`,
        text: value.text,
      }))}
    />
  );
};
