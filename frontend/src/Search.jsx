import React, { useState } from 'react';
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
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Container from '@mui/material/Container';

const SearchPanel = () => {
    const [searching, setSearching] = useState(false);

    const getVideoHandler = async (e) => {
        // const response = await fetch(
        //     url,
        //     {
        //         method : 'GET',
        //         headers: {
        //             'Content-Type': 'application/json'
        //             // 'Content-Type': 'application/x-www-form-urlencoded',
        //           },
        //         body : {}
        //     }
        // ) 
        setSearching(true);
    }

    return (
        <div>
            <SearchAppBar></SearchAppBar>
            {searching && 
            <SearchResultContainer callBack={getVideoHandler}></SearchResultContainer> }
        </div>
    )
}

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

function SearchAppBar(props) {
  const search = props.callback
  return (
    <Box sx={{ flexGrow: 1 }}>
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
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }}
              onKeyUp={search}
            />
          </Search>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

const SearchResultContainer = (props) => {
    // const searchResult = props.resultList()
    const [video, setVideo] = useState(false);
    const testResultList = [{time: 1000, "video_name" : "test name 1"}, {time: 1000, "video_name" : "test name 2"}]
    const toRender = []

    const searchHandler = async (e) => {
        // const response = await fetch(
        //     url,
        //     {
        //         method : 'GET',
        //         headers: {
        //             'Content-Type': 'application/json'
        //             // 'Content-Type': 'application/x-www-form-urlencoded',
        //           },
        //         body : {}
        //     }
        // ) 
        setVideo(true);
    }

    for (const search of testResultList) {
        toRender.push(<ListItem disablePadding>
            <ListItemButton onCLick={searchHandler}>
              <ListItemText primary={search.video_name} />
            </ListItemButton>
          </ListItem>)
        toRender.push(<Divider />)
    }
    return (
        <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
            <List>
                {toRender}
            </List>
            { video && 
            <Container maxWidth="sm">
                <p>This is the container for video.</p>
            </Container>
            }
        </Box>
    )
}

export default SearchPanel;
