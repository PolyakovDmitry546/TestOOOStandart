import AbstractActionForm from "./base-form.js";


class SearchForm extends AbstractActionForm {
    getSearchFieldValue() {
        return this.baseForm.elements["search_field"].value;
    }
    
    getSearchValueValue() {
        return this.baseForm.elements["search_value"].value;
    }

    updateQueryParams() {
        this.parentTable.updateQueryParam("search_field", this.getSearchFieldValue());
        this.parentTable.updateQueryParam("search_value", this.getSearchValueValue());
        this.parentTable.updateQueryParam("page", null);
    }

    updateParentTableHead() {
        this.parentTable.clearUnusedSearchInputs(this.getSearchFieldValue());
    }
}

export default SearchForm;