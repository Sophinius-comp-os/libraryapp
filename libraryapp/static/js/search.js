
    $(document).ready(function () {
        $("#search-input").on("input", function () {
            var query = $(this).val();
            if (query.trim() === "") {
                // Clear the results if the search input is empty
                $("#search-results").empty();
                return;
            }

            $.ajax({
                url: '/search_books/',
                method: 'GET',
                data: {q: query},
                success: function (data) {
                    updateSearchResults(data);
                },
                error: function (error) {
                    console.error('Error searching books:', error);
                }
            });
        });

        function updateSearchResults(data) {
            var resultsContainer = $("#search-results");
            resultsContainer.empty();

            if (data.books && data.books.length > 0) {
                $.each(data.books, function (index, book) {
                    var resultItem = $('<div>').text('Title: ' + book.title + ', Author: ' + book.author);
                    resultsContainer.append(resultItem);
                });
            } else {
                resultsContainer.text('No results found.');
            }
        }
    });

    
    // Your JavaScript code for handling the search click event
    $(document).ready(function () {
        $("#search-input").on("click", function () {
            $("#search-container").load("/search.html");
        });
    });

    