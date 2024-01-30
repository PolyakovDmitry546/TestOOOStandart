import AbstractActionForm from "./base-form.js";


class PaginationForm extends AbstractActionForm {
    getPage() {
        return this.baseForm.elements["page"].value;
    }

    updateQueryParams() {
        this.parentTable.updateQueryParam("page", this.getPage());
    }

}

export default PaginationForm;