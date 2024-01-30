class AbstractActionForm {
    constructor(parentTable, baseForm) {
        this.parentTable = parentTable;
        this.baseForm = baseForm;
        this.extraVariables = {};

        this.boundSubmit = this.submit.bind(this);
        this.baseForm.addEventListener("submit", this.boundSubmit);
    }

    async submit(event) {
        event.preventDefault();
        this.addExtraVariables();
        this.updateQueryParams();
        const responseData = await this.parentTable.sendAjaxRequest();
        this.updateParentTableHead();
        this.parentTable.updateTBody(responseData.object_list);
        this.parentTable.updateNavigation(responseData);
    }

    addExtraVariables() {}

    updateQueryParams() {}

    updateParentTableHead() {}
}

export default AbstractActionForm;