function getOrderingInput(orderingForm) {
    return orderingForm.elements["ordering"];
}

function getOrderingSubmit(orderingForm) {
    let orderingSubmit;
    for (let elem of orderingForm.elements) {
        if (elem.type === "submit") orderingSubmit = elem;
    }
    return orderingSubmit;
}

function getNewOrderingFromForm(orderingForm) {
    return getOrderingInput(orderingForm).value;
}

function reverseOrdering(ordering) {
    if (ordering[0] === "-") {
        ordering = ordering.slice(1);
    }
    else {
        ordering = "-" + ordering;
    };
    return ordering;
}

function getRequestUrl(orderingFrom) {
    const queryParams = new URLSearchParams();
    requisiteTableFilterParameters.forEach((value, key) => {
        if (value !== null) queryParams.append(key, value);
    });
    const queryString = queryParams.toString();
    let requestUrl = orderingFrom.action;
    requestUrl = requestUrl + "?" + queryString;
    return requestUrl;
}

async function sendRequest(requestUrl) {
    const response = await fetch(requestUrl, {
        headers: {
            "x-requested-with": "XMLHttpRequest"
        }
    }).catch(reason => console.log(reason));
    const responseData = await response.json();
    return responseData;
}

function getOrderingSubmitValue(previousValue, ordering) {
    let value;
    if (previousValue.startsWith( "▼") || previousValue.startsWith("▲")) {
        value = previousValue.slice(1);
    }
    else {
        value = previousValue;
    }
    if (ordering.startsWith("-")) {
        value = "▼" + value;
    }
    else {
        value = "▲" + value;
    }
    return value;
}

function updateOrderingFormInputs(orderingForm, ordering) {
    const orderingInput = getOrderingInput(orderingForm);
    const orderingSubmit = getOrderingSubmit(orderingForm);

    orderingSubmit.value = getOrderingSubmitValue(orderingSubmit.value, ordering);
    orderingInput.value = reverseOrdering(ordering);
}

function updateTableData(requisiteList) {
    const table = document.getElementById("requisite-table");
    const tBody = document.createElement("tbody");
    for (let requisite of requisiteList) {
        let tr = document.createElement("tr");
        tr.classList.add("table-info");
        let i = 0;
        for (let field in requisite) {
            let tElem;
            if (i === 0) {
                tElem = document.createElement('th');
                tElem.setAttribute("scope", "row");
                i++;
            }
            else {
                tElem = document.createElement('td');
            }
            tElem.innerText = requisite[field];
            tr.append(tElem);
        }
        tBody.append(tr);
    }
    const oldTBody = table.getElementsByTagName("tbody")[0];
    table.replaceChild(tBody, oldTBody);
}

async function orderingFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    
    let ordering = getNewOrderingFromForm(form);
    requisiteTableFilterParameters.set("ordering", ordering);
    const requestUrl = getRequestUrl(form);
    const responseData = await sendRequest(requestUrl);
    updateOrderingFormInputs(form, ordering);
    updateTableData(responseData.object_list);
    //updateNavigation(response_data)
}

function getSearchField(form) {
    return form.elements["search_field"].value;
}

function getSearchValue(form) {
    return form.elements["search_value"].value;
}

function clearUnusedSearchInputs(usedInputName) {
    const tableHead = document.getElementById("requisite-table-head");
    const searchForms = tableHead.getElementsByClassName("search-form");
    for (let form of searchForms) {
        if (usedInputName !== getSearchField(form)) {
            form.elements["search_value"].value = "";
        }
    }
}

async function searchFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const searchField = getSearchField(form);
    const searchValue = getSearchValue(form);
    requisiteTableFilterParameters.set("search_field", searchField);
    requisiteTableFilterParameters.set("search_value", searchValue);
    const requestUrl = getRequestUrl(form);
    const responseData = await sendRequest(requestUrl);
    clearUnusedSearchInputs(searchField);
    updateTableData(responseData.object_list);
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
const searchForms = tableHead.getElementsByClassName("search-form");
for (let form of searchForms) {
    form.addEventListener("submit", searchFormSubmit);
}