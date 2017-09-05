//http://stackoverflow.com/a/2648463 - wizardry!
String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

//http://stackoverflow.com/a/7616484
String.prototype.hashCode = function() {
    var hash = 0, i, chr, len;
    if (this.length == 0) return hash;
    for (i = 0, len = this.length; i < len; i++) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};

function loadcontests(){
    $('#contests').empty();
    $.post(script_root + "/admin/contests", {
        'nonce': $('#nonce').val()
    }, function (data) {
        contests = $.parseJSON(JSON.stringify(data));


        for (var i = 0; i <= contests['contests'].length - 1; i++) {
            var contest = contests['contests'][i]
            var contest_button = $((
            '<div class="contest-participate__panel">' +
            '    <a style="float: right" class="btn btn-md btn-theme btn-outlined btn-contest" href="' + script_root + '/admin/contest/' + contest.id + '">Edit</a>' +
            '    <h3>#' + contest.id + ' [' + contest.slug + ']' +
            '    </h3><hr>' +
            '    <table class="contest-item-card__table">' +
            '        <tbody>' +
            '            <tr>' +
            '                <td>Contest name:</td>' +
            '                <td>' + contest.name + '</td>' +
            '            </tr>' +
            '            <tr>' +
            '                <td>Start time:</td>' +
            '                <td>' + contest.starttime + '</td>' +
            '            </tr>' +
            '            <tr>' +
            '                <td>End time:</td>' +
            '                <td>' + contest.endtime + '</td>' +
            '            </tr>' +
            '        </tbody>' +
            '    </table>' +
            '</div>'
            ));
            $('#contests').append(contest_button);
        };
    });
}

$(function(){
    loadcontests();
})
