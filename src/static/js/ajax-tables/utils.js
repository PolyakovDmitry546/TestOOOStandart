function getParamFromQueryString(paramName) {
    const query_params = new URLSearchParams(window.location.search);
    if (query_params.has(paramName) && query_params.get(paramName).length > 0) {
        return query_params.get(paramName);
    }
    return null;
}

export default getParamFromQueryString;