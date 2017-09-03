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
            var contest_button = $(('<tr><td>' +
            '<a class="chal-button col-md-2 theme-background" value="{0}" href="/admin/contest/{0}">' +
                '<h5>{1}</h5>' +
                '<br />' +
                '<p class="chal-points"><b>{2}</b></p><br />' +
            '</a>' +
            '</td></tr>').format(contest.id, contest.slug, contest.name));
            $('#contests').append(contest_button);
        };
    });
}

$(function(){
    loadcontests();
})
