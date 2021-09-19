import { useState } from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Container from '@mui/material/Container';
import { VideoPlayer } from './components';

const SearchPanel = () => {
  const [searching, setSearching] = useState(true);
  const [lst, setLst] = useState([]);

  const searchHandler = async (e) => {
    if (e.keyCode === 13) {
      // Cancel the default action, if needed
      e.preventDefault();
      const queryWord = e.target.value;
      console.log(queryWord);

      const response = await fetch(
        'http://10.119.176.254:8000/search?phrase=' + queryWord,
        {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );
      const j = await response.json();
      console.log(j);
      setSearching(true);
      setLst(JSON.parse(JSON.stringify(j)));
    }
  };

  return (
    <Box sx={{ flexGrow: 1, margin: 0, padding: 0 }}>
      <SearchAppBar callBack={searchHandler}></SearchAppBar>
      {searching && (
        <SearchResultContainer searchResult={lst}></SearchResultContainer>
      )}
    </Box>
  );
};

function SearchAppBar(props) {
  const search = props.callBack;
  return (
    <Box sx={{ flexGrow: 1, margin: 0, padding: 0 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
          >
            Library
          </Typography>
          <Search onKeyDown={(e) => search(e)} tabIndex="0">
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }}
            />
          </Search>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

const SearchResultContainer = (props) => {
  const searchResult = props.searchResult;
  // const testResultList = [{time: 1000, "video_name" : "test name 1"}, {time: 1000, "video_name" : "test name 2"}]
  const toRender = [];
  const [video, setVideo] = useState(false);
  const [path, setPath] = useState('');
  const [time, setTime] = useState(0);

  const handlePlayerReady = (player) => {};

  const getVideoHandler = async (n, time) => {
    if (video) {
      setVideo(false);
      return;
    }
    const name = n;
    console.log(name);
    setVideo(true);
    setPath('http://10.119.176.254:8000/storage/' + name);
    setTime(time);
    console.log(path);
    // const response = await fetch(
    //     "http://10.119.176.254:8000/storage/" + name,
    //     {
    //         method : 'GET',
    //     }
    // )
    // const j = await response.json()
    // console.log(j)
  };
  let keyIndex = 0;
  for (const search of searchResult) {
    toRender.push(
      <ListItem
        disablePadding
        key={keyIndex}
        onClick={(e) =>
          getVideoHandler(search.video_name, search.timestamp / 1000)
        }
      >
        <ListItemButton key={keyIndex}>
          <ListItemText
            primary={search.video_name}
            key={keyIndex}
            insect={true}
            secondary={'timestamp :' + search.timestamp / 1000 + ' sec'}
          />
        </ListItemButton>
      </ListItem>,
    );
    toRender.push(<Divider />);
    keyIndex += 1;
  }
  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
        display: 'flex',
        flexDirection: 'row',
      }}
    >
      <Box sx={{ width: '30%' }}>
        <List>{toRender}</List>
      </Box>
      {video && (
        <Container maxwidth="sm">
          {/* <video width="800" height="600" controls={true} autoplay={true}>
                    <source src={path} type="video/mp4" />
                    Your browser does not support the video tag.
                </video> */}
          <VideoPlayer
            onReady={handlePlayerReady}
            options={{
              fluid: true,
              controls: true,
              sources: [{ src: path, type: 'video/mp4' }],
              width: 800,
            }}
            curTime={time}
          />
        </Container>
      )}
    </Box>
  );
};

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  padding: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const VideoContainer = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  marginRight: 0,
  marginLeft: 'auto',
  height: '100%',
  position: 'relative',
  pointerEvents: 'none',
  display: 'flex',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));
export default SearchPanel;
