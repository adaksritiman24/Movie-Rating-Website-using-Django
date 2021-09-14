console.log('console working');
$('#watchbtn').click(() => {
    console.log('click worked');
    if (document.getElementById('watchbtn').innerText === 'Add to WatchList') {
        //to be added to watchlist
        console.log('To be added');
        $.ajax({
            url: 'addtowatchlist/',
            method: "GET",
            // data: {
            //     movie: document.getElementById('movie-hidden').innerText,
            //     viewer: document.getElementById('viewer-hidden').innerText,
            // },
            // datatype : 'json',
            success: function (data) {
                console.log(data);
                document.getElementById('watchbtn').innerText = 'Remove from WatchList';
            }
        })
    }

    else {
        console.log('To be removed');
        $.ajax({
            url: 'removefromwatchlist/',
            method: "GET",

            success: function (data) {
                console.log(data);
                document.getElementById('watchbtn').innerText = 'Add to WatchList';
            }
        })
    }

})

$('#submitrating').click(() => {
    // console.log('Submit rating clicked');
    rating = document.getElementById('ratingselect').value;
    console.log(rating);
    if (rating !== 'N') {
        ratingdata = {
            rat: rating,
        }
        $.ajax({
            url: "submitrating/",
            method: 'POST',
            data: ratingdata,
            datatype: 'json',
            success: (data) => {
                console.log(data);
                document.getElementById('you-rated').style.display = "block";
                document.getElementById('you-rated').innerText = "You rated : " + rating;
                try {
                    document.getElementById('rm-rt-temp').classList.remove('hide');
                }
                catch (Exception) {
                    //pass
                    document.getElementById('rm-rt').style.display = 'inline-block';
                }
            }
        })
    }
});

$('#removerating').click(() => {
    console.log('remove rating');
    $.ajax({
        url: "removerating/",
        method: 'GET',
        datatype: 'json',
        success: (data) => {
            console.log(data);
            try {
                document.getElementById('rm-rt').style.display = 'none';
            }
            catch (Exception) {
                document.getElementById('rm-rt-temp').classList.add('hide');
            }

            document.getElementById('you-rated').style.display = 'none';
        }
    })

});

$('#favbtn').click(() => {
    console.log('click worked');
    if (document.getElementById('favbtn').innerText === 'Add to Favourites') {
        //to be added to watchlist
        console.log('To be added');
        $.ajax({
            url: 'addtofavourites/',
            method: "GET",

            success: function (data) {
                console.log(data);
                document.getElementById('favbtn').innerText = 'Remove from Favourites';
            }
        })
    }

    else {
        console.log('To be removed');
        $.ajax({
            url: 'removefromfavourites/',
            method: "GET",

            success: function (data) {
                console.log(data);
                document.getElementById('favbtn').innerText = 'Add to Favourites';
            }
        })
    }
})
//movie review submissions and deletions
$('#postreview').click(() => {

    review = document.getElementById('reviewbox').value
    if (!review == "") {
        console.log('Posting review..' + review)
        myreview = { review: review }
        $.ajax({
            url: "postreview/",
            method: 'POST',
            datatype: 'json',
            data: myreview,
            success: (data) => {
                console.log(data);
                try {
                    box = document.getElementById('my-rev');
                    // h5 = box.getElementsByTagName('h5')[0]
                    label = box.getElementsByTagName('label')[0];
                    p = box.getElementsByTagName('p')[0];
                    p.innerText = review;
                    label.innerText = data.time;
                    box.classList.remove('hide');
                } catch (Exception) {
                    box = document.getElementById('my-rev-temp');
                    label = box.getElementsByTagName('label')[0];
                    p = box.getElementsByTagName('p')[0];
                    p.innerText = review;
                    label.innerText = data.time;
                    box.classList.remove('hide');
                }
                document.getElementById('reviewbox').value = "";
            }
        })
    }
})
$('#deletereview').click(() => {
    console.log('Deleting review..')
    $.ajax({
        url: 'deletereview/',
        method: 'GET',
        datatype: 'json',
        success: (data) => {
            console.log(data);
            try {
                document.getElementById('my-rev').classList.add('hide');
            }
            catch (Exception) {
                document.getElementById('my-rev-temp').classList.add('hide');
            }
        }
    })
})