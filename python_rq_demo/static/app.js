$(document).ready(() => {

    if (window.toastr) {
        window.toastr.options = {
            closeButton: true,
            extendedTimeout: 0,
            hideDuration: 250,
            hideEasing: "linear",
            hideMethod: "fadeOut",
            newestOnTop: true,
            positionClass: "toast-top-right",
            preventDuplicates: true,
            showDuration: 250,
            showEasing: "linear",
            showMethod: "fadeIn",
            timeOut: 0,
        };
    }


    window.app = window.app || {};


    window.app.checkForUpdates = async () => {
        let jobs = app.getJobs();
        let promises = jobs.map(async (job) => {
            if (['failed', 'finished'].indexOf(job.status) >= 0) {
                return job;
            }
            else {
                let uri = `/api/job_status/${job.id}`;
                let result = await app.getJSON(uri);
                job.status = result.status;
                job.title = result.title;
                job.message = result.message;
                job.duration = result.duration;
                switch (job.status) {
                case 'failed':
                    toastr.error(job.message, job.title)
                    break;
                case 'finished':
                    toastr.success(job.message, job.title);
                    break;
                case 'no_such_job':
                    let index = jobs.indexOf(job);
                    jobs.splice(index, 1);
                    break;
                }
                return job;
            }
        });
        await Promise.all(promises);
        app.saveJobs(jobs);
        return jobs;
    };


    window.app.getJobs = () => {
        let jobsItem = window.localStorage.getItem("jobs");
        if (jobsItem) {
            return JSON.parse(jobsItem);
        }
        else {
            return [];
        }
    }


    window.app.getJSON = async (uri) => {
        let options = {
            method: "GET",
            mode: "cors"
        };
        let response = await fetch(uri, options)
        if (response.ok) {
            return response.json();
        }
        else {
            console.warn(response);
            return {};
        }
    }


    window.app.postJSON = async (uri, data) => {
        let options = {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(data)
        };
        let response = await fetch(uri, options);
        if (response.ok) {
            return response.json();
        }
        else {
            console.warn(response);
            return {};
        }
    }


    window.app.saveJobs = (jobs) => {
        let jobsString = JSON.stringify(jobs);
        window.localStorage.setItem("jobs", jobsString);
    }


    window.app.syncJobs = async () => {
        jobs = app.getJobs();
        let result = await app.getJSON('/api/jobs');
        let addCount = 0;
        result.job_ids.forEach(id => {
            let existingJob = jobs.find(j => j.id === id);
            if (!existingJob) {
                jobs.push({
                    id: id
                });
                addCount += 1;
            }
        });
        if (addCount > 0) {
            console.log(`syncJobs added ${addCount} jobs to the local database`);
        }
        app.saveJobs(jobs);
    };


    app.syncJobs();
    setInterval(app.syncJobs, 60 * 1000);
    setInterval(app.checkForUpdates, 5 * 1000);

});
