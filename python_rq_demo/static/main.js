$(document).ready(() => {

    const $deleteFailedJobs = $("#delete-failed-jobs");
    const $form = $("form");

    function getFormData() {
        return {
            message: $('textarea[name="message"]').val(),
            sleep_duration: $('input[name="sleep_duration"]').val()
        };
    }

    function getRequestOpts(method = "POST", data = undefined) {
        let opts = {
            headers: {
                "Content-type": "application/json"
            },
            method: method,
            mode: "cors"
        }
        if (data) {
            opts.body = JSON.stringify(data);
        }
        return opts;
    }


    $deleteFailedJobs.on("click", async (e) => {
        let opts = getRequestOpts("POST")
        let response = await fetch("/api/delete_failed_jobs", opts);
        if (response.ok) {
            let result = await response.json();
            if (result.count === 0) {
                toastr.success("Call was successful, but there were no jobs to delete.");
            }
            else if (result.count === 1) {
                toastr.success(`Deleted ${result.count} failed job.`);
            }
            else {
                toastr.success(`Deleted ${result.count} failed jobs.`);
            }
            return Promise.resolve(result);
        }
        else {
            return Promise.reject(response);
        }
    });

    $form.on("submit", async (e) => {
        e.preventDefault();
        e.stopPropagation();

        let data = getFormData();
        let opts = getRequestOpts("POST", data);
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
