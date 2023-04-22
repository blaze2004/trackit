window.addEventListener('scroll', function() {
    let header = document.querySelector('header');
    let windowlPosition = window.scrollY > 0;
    header.classList.toggle('scrolling-active', windowlPosition);
});
function saveToDatabase(attendanceData) {

    url = window.location.origin + "/mac/save-attendance/";

    if (attendanceData != null && attendanceData != undefined && attendanceData != "undefined") {
        $.ajax({
            url: url,
            type: "POST",
            data: {
                'latest_meet_attendance': attendanceData
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
            },
            cache: false,
            success: function(response) {
                var recordId = response["record_id"];
                if (window.location.pathname == "/mac/save/" || window.location.pathname == "/mac/save/#") {
                    window.location.href = window.location.origin + "/mac/report-view/" + recordId + "/";
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}

function save_data() {

    let _data = localStorage.getItem('latest_meet_attendance');
    saveToDatabase(_data);
};

function saveAttendanceReport(key, attendanceData) {

    url = window.location.origin + "/save-attendance-report/";

    if (attendanceData != null && attendanceData != undefined && attendanceData != "undefined") {
        $.ajax({
            url: url,
            type: "POST",
            data: {
                'latest_meet_attendance': attendanceData
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            },
            cache: false,
            success: function(response) {
                var reportUrl = response["url"];
                localStorage.removeItem(key);
                if (window.location.pathname == "/mac/save/" || window.location.pathname == "/mac/save/#") {
                    window.location.href = reportUrl;
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}

function saveAttendance() {

    save_data();
    var i, report, reports = [];
    const query = RegExp('meet_attendance_report_');

    for (i in localStorage) {
        if (localStorage.hasOwnProperty(i)) {
            if (i.match(query) || (!query && typeof i === 'string')) {
                value = JSON.parse(localStorage.getItem(i));
                reports.push({
                    key: i,
                    data: value
                });
            }
        }
    }

    reports.forEach(report => {
        saveAttendanceReport(report.key, JSON.stringify(report.data));
    });
}

window.addEventListener('load', function() {
    setTimeout(saveAttendance, 2000);
});