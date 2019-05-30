$(document).ready(() => {

    const $form = $("form");

    $form.on("submit", async (e) => {
        e.preventDefault();
        e.stopPropagation();

        let data = {
            message: $('textarea[name="message"]').val(),
            sleep_duration: $('input[name="sleep_duration"]').val()
        };

        let opts = {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(data)
        }

        let response = await fetch('/api/messages', opts);
        if (response.ok) {
            let job = await response.json();
            console.log("new job:", job);
            let jobsItem = localStorage.getItem("jobs");
            let jobs = (jobsItem) ? JSON.parse(jobsItem) : [];
            jobs.push(job);
            localStorage.setItem("jobs", JSON.stringify(jobs));
            return Promise.resolve(job);
        }
        else {
            return Promise.reject(response);
        }

    });

});
