$(document).ready(() => {

    // How frequently should the job list be synced with the
    // server? A smaller interval takes more server resources,
    // but responds to updates more quickly.
    const syncInterval = 3 * 1000;

    const $jobsTable = $("#jobs-table-body");

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
        job.previousStatus = job.status;
        job.status = result.status;
        job.title = result.title;
        job.message = result.message;
        job.duration = result.duration;
        return job;
    }

    function getFriendlyDuration(value) {
        if (!value) {
            return "NA seconds";
        }
        else if (typeof value !== "number") {
            return "NA seconds";
        }
        else if (value > 6000) {
            return `about ${Math.round(value / (3600))} hours`;
        }
        else if (value > 45) {
            return `about ${Math.round(value / 60)} minutes`;
        }
        else {
            return `${Math.round(value)} seconds`;
        }
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

    function showJobNotification(job) {
        // console.log("show job notification:", job);
        if (job.status === "failed") {
            toastr.error(job.message || `Job ${job.id} failed. Please see the server logs for more info.`, job.title || "Failed Job");
        }
        else if (job.status === "finished") {
            toastr.success(`${job.message}<br>Duration: ${getFriendlyDuration(job.duration)}.`, job.title);
        }
        else if (job.status !== job.previousStatus) {
            toastr.info(`Job status: ${job.status}`, "Job Status Changed");
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

            // If we already know the status, and the status is "failed"
            // or "finished", then there is nothing more to do. Otherwise,
            // check the job for updates and display a notification.
            if (["failed", "finished"].indexOf(job.status) === -1) {
                await checkJobForUpdates(job);
                showJobNotification(job);
            }
        }

        saveLocalJobs(mergedJobs);
        updateJobsTable(mergedJobs);
    }

    function updateJobsTable(jobs) {
        $jobsTable.children().remove();
        for (let i = 0; i < jobs.length; i++) {
            let job = jobs[i];
            let tr = "";
            tr += `<tr id="job-${job.id}">\n`;
            tr += `    <td>${job.id}</td>\n`;
            tr += `    <td>${job.message}</td>\n`;
            tr += `    <td>${job.title}</td>\n`;
            tr += `    <td>${job.status}</td>\n`;
            tr += `    <td>${getFriendlyDuration(job.duration)}</td>\n`;
            tr += "</tr>\n";
            $jobsTable.append(tr);
        }
    }

    setInterval(() => {
        syncJobs();
    }, syncInterval);

});
