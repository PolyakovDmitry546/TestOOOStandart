import AbstractActionForm from "./base-form.js";


class OrderingForm extends AbstractActionForm {
    getNewOrdering() {
        return this.baseForm.elements["ordering"].value;
    }

    addExtraVariables() {
        this.extraVariables.ordering = this.getNewOrdering();
    }

    updateQueryParams() {
        this.parentTable.updateQueryParam("ordering", this.extraVariables.ordering);
        this.parentTable.updateQueryParam("page", null);
    }

    getOrderingInput() {
        return this.baseForm.elements["ordering"];
    }

    getOrderingSubmit() {
        let orderingSubmit;
        for (let elem of this.baseForm.elements) {
            if (elem.type === "submit") orderingSubmit = elem;
        }
        return orderingSubmit;
    }

    reverseOrdering(ordering) {
        let newOrdering;
        if (ordering.startsWith("-")) {
            newOrdering = ordering.slice(1);
        }
        else {
            newOrdering = "-" + ordering;
        };
        return newOrdering;
    }

    getOrderingSubmitValue(previousValue, ordering) {
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

    updateInputs() {
        const orderingInput = this.getOrderingInput();
        const orderingSubmit = this.getOrderingSubmit();
        const ordering = this.extraVariables.ordering;
    
        orderingSubmit.value = this.getOrderingSubmitValue(orderingSubmit.value, ordering);
        orderingInput.value = this.reverseOrdering(ordering);
    }

    updateParentTableHead() {
        this.updateInputs();
        this.parentTable.clearUnusedOrderingDirection(this.getNewOrdering());
    }
}

export default OrderingForm;