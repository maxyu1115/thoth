import { Tab, Tabs, Typography } from '@mui/material';
import { Box } from '@mui/system';
import { useState } from 'react';
import { CustomDropzone } from './components';
import SearchPanel from './Search';

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
      hidden={value != index}
      id={`thoth-tabpanel-${index}`}
      aria-labelledby={`thoth-tabpanel-${index}`}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
};

const App = (): JSX.Element => {
  const [value, setValue] = useState(0);
  const [videoUrl, setVideoUrl] = useState('');

  const handleTabChange = (
    event: React.SyntheticEvent,
    newValue: number,
  ): void => {
    event.preventDefault();
    setValue(newValue);
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
          <video controls src={videoUrl} />
        )}
      </TabPanel>
      <TabPanel value={value} index={1}>
        Item Two
      </TabPanel>
      <TabPanel value={value} index={2}>
        Item Three
      </TabPanel>
      <TabPanel value={value} index={3}>
        <SearchPanel></SearchPanel>
      </TabPanel>
    </Box>
  );
};

export default App;
