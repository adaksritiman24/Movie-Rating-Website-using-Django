function movie_search(type){
    console.log('clicked');
    movies = document.getElementsByClassName('movie-selector')
    for(movie of movies){
        movie.classList.remove("hide");
        genre = movie.getElementsByClassName('card')[0]
            .getElementsByClassName('card-body')[0]
            .getElementsByClassName('genre-info')[0]
            .innerText;
        if(!genre.toLowerCase().includes(type)){
            movie.classList.add('hide');
        }
        
    }
}
function movie_search_by_lang(type){
    movies = document.getElementsByClassName('movie-selector')
    for(movie of movies){
        movie.classList.remove("hide");
        lang = movie.getElementsByClassName('card')[0]
            .getElementsByClassName('card-body')[0]
            .getElementsByClassName('lang-info')[0]
            .innerText;
        if(!lang.toLowerCase().includes(type)){
            movie.classList.add('hide');
        }
        
    }
}


function searchMovieByName(){
    // console.log('search Working');
    movies = document.getElementsByClassName('movie-selector')
    if(movies.length!== 0){
        movie_title = document.getElementById('moviebar').value
        for(movie of movies){
            movie.classList.remove("hide");
            nm = movie.getElementsByClassName('card')[0]
                .getElementsByClassName('card-body')[0]
                .getElementsByClassName('card-title')[0]
                .innerText;
            if(!nm.toLowerCase().includes(movie_title.toLowerCase())){
                movie.classList.add('hide');
            }
            
        }
    }
    
}
$('#moviebar').keyup(searchMovieByName);
console.log('here');