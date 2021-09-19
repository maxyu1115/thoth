import { Button, Tab, Tabs } from '@mui/material';
import { Box } from '@mui/system';
import SearchPanel from './Search';
import { useRef, useState } from 'react';
import { VideoJsPlayer } from 'video.js';
import { CustomDropzone, Slides, VideoPlayer } from './components';

const a11yProps = (index: number): any => ({
  id: `thoth-tab-${index}`,
  'aria-controls': `thoth-tabpanel-${index}`,
});

const TabPanel = ({
  children,
  index,
  value,
}: {
  children?: React.ReactNode;
  index: number;
  value: number;
}): JSX.Element => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`thoth-tabpanel-${index}`}
      aria-labelledby={`thoth-tabpanel-${index}`}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const App = (): JSX.Element => {
  const [value, setValue] = useState(0);
  const [videoUrl, setVideoUrl] = useState('');

  const playerRef = useRef<VideoJsPlayer | null>(null);

  const handleTabChange = (
    event: React.SyntheticEvent,
    newValue: number,
  ): void => {
    event.preventDefault();
    setValue(newValue);
  };

  const handlePlayerReady = (player: VideoJsPlayer): void => {
    playerRef.current = player;
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={value}
          onChange={handleTabChange}
          aria-label="basic options for thoth"
        >
          <Tab label="Upload Video" {...a11yProps(0)} />
          <Tab label="View Transcript" {...a11yProps(1)} />
          <Tab label="View Slides" {...a11yProps(2)} />
          <Tab label="Key Word Search" {...a11yProps(3)} />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        {videoUrl === '' ? (
          <CustomDropzone setter={setVideoUrl} />
        ) : (
          <>
          <VideoPlayer
            onReady={handlePlayerReady}
            options={{
              controls: true,
              sources: [{ src: videoUrl, type: 'video/mp4' }],
            }}
          />
          <Button onClick={() => playerRef.current?.currentTime(87)} variant="contained">Skip</Button>
          </>
        )}
      </TabPanel>
      <TabPanel value={value} index={1}>
        Item Two
      </TabPanel>
      <TabPanel value={value} index={2}>
        <Slides
          slides={[
            {
              order: 0,
              path: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Petauroides_volans.jpg/800px-Petauroides_volans.jpg',
              text: 'MUCH MUCH MUCH text here',
            },
            {
              order: 1,
              path: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Our_Lady_of_La_Salette.jpg/1024px-Our_Lady_of_La_Salette.jpg',
              text: 'Lots of text here too',
            },
          ]}
        />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <SearchPanel></SearchPanel>
      </TabPanel>
    </Box>
  );
};

export default App;
