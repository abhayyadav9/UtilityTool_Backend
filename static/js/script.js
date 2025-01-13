$(document).ready(function () {
    $('#fetch-resolutions').click(function () {
        const url = $('#url').val();
        if (!url) {
            alert("Please enter a valid URL");
            return;
        }
        $.post('/get_resolutions', { url }, function (data) {
            if (data.error) {
                alert(data.error);
                return;
            }
            const resolutionDropdown = $('#resolution');
            resolutionDropdown.empty();
            data.resolutions.forEach(res => {
                resolutionDropdown.append(`<option value="${res}">${res}</option>`);
            });
            $('#resolutions').show();
        });
    });

    $('#download').click(function () {
        const url = $('#url').val();
        const resolution = $('#resolution').val();
        if (!resolution) {
            alert("Please select a resolution");
            return;
        }
        $.post('/download', { url, resolution }, function (data) {
            if (data.error) {
                alert(data.error);
                return;
            }
            $('#message').text(data.message);
        });
    });
});
