import getParamFromQueryString from "./utils.js";
import OrderingForm from "./ordering-form.js";
import SearchForm from "./search-form.js";
import PaginationForm from "./pagination-from.js";


class RequisiteTable {
    queryParams = new Map();

    constructor() {
        this.initQueryParams();
        this.initTableParts();
        this.initActionForms();
    }

    initQueryParams() {
        this.updateQueryParam("ordering", getParamFromQueryString("ordering"));
        this.updateQueryParam("search_field", getParamFromQueryString("search_field"));
        this.updateQueryParam("search_value", getParamFromQueryString("search_value"));
        this.updateQueryParam("page", getParamFromQueryString("page"));
    }

    initTableParts() {
        this.table = document.getElementById("requisite-table");
        this.thead = document.getElementById("requisite-table-head");
        this.paginationNavbar = document.getElementById("pagination-navbar");
    }

    initActionForms() {
        const orderingForms = this.thead.getElementsByClassName("ordering-form");
        const searchForms = this.thead.getElementsByClassName("search-form");
        
        this.orderingForms = [];
        for (let form of orderingForms) {
            this.orderingForms.push(new OrderingForm(this, form));
        }
        this.searchForms = [];
        for (let form of searchForms) {
            this.searchForms.push(new SearchForm(this, form));
        }
        this.createPaginationForms();
    }

    updateQueryParam(key, value) {
        this.queryParams.set(key, value);
    }

    createPaginationForms() {
        const paginationForms = this.paginationNavbar.getElementsByTagName("form");
        this.paginationForms = [];
        for (let form of paginationForms) {
            this.paginationForms.push(new PaginationForm(this, form));
        }
    }

    getBaseRequestUrl() {
        return window.location.pathname;
    }

    getRequestUrl() {
        const queryParams = new URLSearchParams();
        this.queryParams.forEach((value, key) => {
            if (value !== null) queryParams.append(key, value);
        });
        const queryString = queryParams.toString();
        const requestUrl = this.getBaseRequestUrl() + "?" + queryString;
        return requestUrl;
    }

    async sendAjaxRequest() {
        const requestUrl = this.getRequestUrl();
        const response = await fetch(requestUrl, {
            headers: {
                "x-requested-with": "XMLHttpRequest"
            }
        }).catch(reason => console.log(reason));
        const responseData = await response.json();
        return responseData;
    }

    updateTBody(requisiteList) {
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
        const oldTBody = this.table.getElementsByTagName("tbody")[0];
        this.table.replaceChild(tBody, oldTBody);
    }

    clearUnusedOrderingDirection(usedOrdering) {
        for (let form of this.orderingForms) {
            if (usedOrdering !== form.getNewOrdering()) {
                let submit = form.getOrderingSubmit();
                if (submit.value.startsWith( "▼") || submit.value.startsWith("▲")) {
                    submit.value = submit.value.slice(1);
                }
            }
        }
    }

    clearUnusedSearchInputs(usedInputName) {
        for (let form of this.searchForms) {
            if (usedInputName !== form.getSearchFieldValue()) {
                form.baseForm.elements["search_value"].value = "";
            }
        }
    }

    _createPaginationItem(pageText, pageNumber) {
        const li = document.createElement("li");
        li.classList.add("page-item");
        const pageForm = document.createElement("form");
        pageForm.action = window.location.pathname;
        pageForm.method = "get";
        const submit = document.createElement("input");
        submit.type = "submit";
        submit.classList.add("page-link");
        submit.value = pageText;
        const hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.name = "page";
        hidden.value = pageNumber;
        pageForm.append(submit, hidden);
        li.append(pageForm);
        return li;
    }

    updateNavigation(pageObj) {
        const oldUl = this.paginationNavbar.getElementsByTagName("ul")[0];
        const newUl = document.createElement("ul");
        newUl.classList.add("pagination");
        if (pageObj.has_other_pages) {
            if (pageObj.has_previos) {
                newUl.append(this._createPaginationItem("«", 1));
                newUl.append(this._createPaginationItem("назад", pageObj.page - 1));
            }
            const li = document.createElement("li");
            li.classList.add("page-item");
            const span = document.createElement("span");
            span.classList.add("page-link");
            span.textContent = pageObj.page + " из " + pageObj.num_pages;
            li.append(span);
            newUl.append(li);
            if (pageObj.has_next) {
                newUl.append(this._createPaginationItem("далее", pageObj.page + 1));
                newUl.append(this._createPaginationItem("»", pageObj.num_pages));
            }
        }
        this.paginationNavbar.replaceChild(newUl, oldUl);
        this.createPaginationForms();
    }
}

export default RequisiteTable;