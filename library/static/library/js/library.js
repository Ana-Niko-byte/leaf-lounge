document.addEventListener("DOMContentLoaded", () => {
    /**
     * Sets the background colour of each book once DOM content loads.
     */
    const books = [...document.getElementsByClassName("book-spine")];
    const colours = ["#072743","#11395E","#12213F","#066886","#0291B5","#B700E1"];

    for (let book of books){
        let randomIndex = Math.floor(Math.random() * 6);
        if (book.style.backgroundColor !== 'white'){
            book.style.backgroundColor = `${colours[randomIndex]}`;
        }
    }

    const fullBooks = [...document.getElementsByClassName("book")];
    fullBooks.forEach(book => {
        book.addEventListener("mouseover", () => {
            fullBooks.forEach(otherBook => {
                if (otherBook !== book) {
                    otherBook.style.zIndex = '20';
                    console.log(otherBook.style.zIndex);
                }
            });
        });
    })
})