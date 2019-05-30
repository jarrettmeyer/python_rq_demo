$(document).ready(() => {

    const syncInterval = 15 * 1000;

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

    async function checkJobForUpdates(job) {
        let result = await getJSON(`/api/job_status/${job.id}`);
        job.status = result.status;
        job.title = result.title;
        job.message = result.message;
        job.duration = result.duration;
        return job;
    }

    async function getJSON(uri) {
        let options = {
            method: "GET",
            mode: "cors"
        };
        let response = await fetch(uri, options);
        if (response.ok) {
            return await response.json();
        }
        return Promise.reject(response);
    }

    function getLocalJobs() {
        let jobsItem = localStorage.getItem("jobs");
        if (jobsItem) {
            return JSON.parse(jobsItem);
        }
        return [];
    }

    async function getServerJobs() {
        let result = await getJSON('/api/jobs');
        let jobs = result.job_ids.map(id => {
            return {
                id: id,
                status: null
            };
        });
        // console.log("server jobs:", jobs);
        return jobs;
    }

    function saveLocalJobs(jobs) {
        let jobsString = JSON.stringify(jobs);
        localStorage.setItem("jobs", jobsString);
    }

    function showJob(job) {
        switch (job.status) {
        case "failed":
            toastr.error(job.message, job.title);
            break;
        case "finished":
            toastr.success(job.message, job.title);
            break;
        default:
            // Do nothing.
            break;
        }
    }

    async function syncJobs() {
        let localJobs = getLocalJobs();
        let remoteJobs = await getServerJobs();

        let mergedJobs = [];
        for (let i = 0; i < remoteJobs.length; i++) {
            let remoteJob = remoteJobs[i];
            let job = localJobs.find(job => job.id === remoteJob.id);
            if (!job) {
                job = remoteJob;
                console.log(`Adding new job ${job.id} to local array.`);
            }
            mergedJobs.push(job);

            if (["failed", "finished"].indexOf(job.status) === -1) {
                await checkJobForUpdates(job);
                showJob(job);
            }
        }

        saveLocalJobs(mergedJobs);
    }

    setInterval(() => {
        syncJobs();
    }, syncInterval);

});
