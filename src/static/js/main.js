async function orderingFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    let requestUrl = form.action;
    let ordering = form.elements["ordering"].value;
    if (ordering[0] === "-") {
        ordering = ordering.slice(1);
    }
    else {
        ordering = "-" + ordering;
    };
    //changeOrdering()
    requisiteTableFilterParameters.set("ordering", ordering);
    const queryParams = new URLSearchParams();
    requisiteTableFilterParameters.forEach((value, key) => {
        if (value !== null) queryParams.append(key, value);
    });
    const queryString = queryParams.toString();
    requestUrl = requestUrl + "?" + queryString;
    const response = await fetch(requestUrl, {
        headers: {
            "x-requested-with": "XMLHttpRequest"
        }
    }).catch(reason => console.log(reason));
    response_data = await response.json();
    //updateTable(response_data)
    //updateNavigation(response_data)
}

function getFilterParameterFromQuery(paramName) {
    const query_params = new URLSearchParams(window.location.search);
    if (query_params.has(paramName) && query_params.get(paramName).length > 0) {
        return query_params.get(paramName);
    }
    return null;
}
 
const requisiteTableFilterParameters = new Map();
requisiteTableFilterParameters.set("ordering", getFilterParameterFromQuery("ordering"));
requisiteTableFilterParameters.set("search_field", getFilterParameterFromQuery("search_field"));
requisiteTableFilterParameters.set("search_value", getFilterParameterFromQuery("search_value"));
requisiteTableFilterParameters.set("page", getFilterParameterFromQuery("page"));


const tableHead = document.getElementById("requisite-table-head");
const orderingForms = tableHead.getElementsByClassName("ordering-form");
for (let form of orderingForms) {
    form.addEventListener("submit", orderingFormSubmit);
}