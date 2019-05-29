$(document).ready(() => {

    const $form = $("form");
    const submitURI = "/api/messages";

    $form.on("submit", (e) => {
        e.preventDefault();
        e.stopPropagation();

        let data = {
            message: $('textarea[name="message"]').val(),
            sleep_duration: $('input[name="sleep_duration"]').val()
        };

        app.postJSON(submitURI, data)
            .then((result) => {
                let jobs = app.getJobs();
                jobs.push({
                    id: result.id,
                    status: result.status
                });
                app.saveJobs(jobs);
            });
    });

});
