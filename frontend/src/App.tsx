import { Tab, Tabs } from '@mui/material';
import { Box } from '@mui/system';
import SearchPanel from './Search';
import { useState } from 'react';
import { PreviewUpload, SlidePanel } from './pages';

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

const TabPanelWithNoPadding = ({
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
      {value === index && <Box sx={{ p: 0 }}>{children}</Box>}
    </div>
  );
};

const App = (): JSX.Element => {
  const [value, setValue] = useState(0);
  const [videoName, setVideoName] = useState('');

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
        <PreviewUpload
          onUploadFinish={(name: string): void => setVideoName(name)}
        />
      </TabPanel>
      <TabPanel value={value} index={1}>
        Item Two
      </TabPanel>
      <TabPanel value={value} index={2}>
        <SlidePanel videoName={videoName} />
      </TabPanel>
      <TabPanelWithNoPadding value={value} index={3}>
        <SearchPanel></SearchPanel>
      </TabPanelWithNoPadding>
    </Box>
  );
};

export default App;
