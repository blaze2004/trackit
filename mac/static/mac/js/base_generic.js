window.addEventListener('scroll', function() {
    let header = document.querySelector('header');
    let windowlPosition = window.scrollY > 0;
    header.classList.toggle('scrolling-active', windowlPosition);
});

function save_data() {

    let _data = localStorage.getItem('latest_meet_attendance');

    if (_data != null && _data != 'undefined' && _data != undefined) {

        $.ajax({

            // url: "https://trackitnow.pythonanywhere.com/mac/save-attendance/",
            url: "https://trackit-webapp.herokuapp.com/mac/save-attendance/",
            type: "POST",
            data: {
                'latest_meet_attendance': _data
            },
            cache: false,
            success: function(response) {
                var record_id = response['record_id'];
                localStorage.removeItem('latest_meet_attendance');
                console.log('Attendance saved to database.');
                if (window.location.href == 'https://trackit-webapp.herokuapp.com/mac/save/') {
                    window.location.href = 'https://trackit-webapp.herokuapp.com/mac/report-view/?id=' + record_id;
                }
                // if (window.location.href == 'https://trackitnow.pythonanywhere.com/mac/save/') {
                //     window.location.href = 'https://trackitnow.pythonanywhere.com/mac/report-view/?id=' + record_id;
                // }
            },
            error: function(response) {
                console.log(response);
            }

        });

    }
};
window.addEventListener('load', save_data);