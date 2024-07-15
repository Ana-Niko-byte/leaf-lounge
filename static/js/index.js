document.addEventListener("DOMContentLoaded", () => {
    /**
     * Dynamically sets the copyright year.
     * 
     * Method:
     * On DOM content load, retrieves the "copyright-year" span element.
     * Retrieves the current year.
     * Sets the innertext of the span element to the current year.
     */
    const copyrightYear = document.getElementById("copyright-year");
    const yearNow = new Date().getFullYear();

    copyrightYear.innerText = yearNow;
});