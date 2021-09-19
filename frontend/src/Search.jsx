import React from 'react';

const SearchPanel = () => {
    return (
        <div>
            <p> This is the search panel container </p>
            <SearchBar></SearchBar>
            <SearchResultContainer></SearchResultContainer>
        </div>
    )
}

const SearchBar = () => {
    return (
    <form action="/" method="get">
        <label htmlFor="header-search">
            <span className="visually-hidden">Search key words </span>
        </label>
        <input
            type="text"
            id="header-search"
            placeholder="Search blog posts"
            name="s" 
        />
        <button type="submit">Search</button>
    </form>)
}

const SearchResultContainer = (props) => {
    // const searchResult = props.resultList()
    const testResultList = [{time: 1000, "video_name" : "test name 1"}, {time: 1000, "video_name" : "test name 2"}]
    const toRender = []
    for (const search of testResultList) {
        toRender.push(<SearchResultEntry data={search}></SearchResultEntry>)
    }
    return (
        <div>
            {toRender}
        </div>
    )
}

const SearchResultEntry = (props) => {
    const time = props.data.timestamp
    const videoName = props.data.video_name
    return (
        <div>
            <div><p>{videoName} ":" {time} </p></div>
        </div>
    )
}

export default SearchPanel;