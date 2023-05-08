let hostname = (new URL(window.location.href)).origin
// let protocol = (new URL(window.location.href)).protocol

if(hostname.includes('localhost')) {
    hostname = 'http://trailersplus.viewdemo.co' 
}

export default {
    env: {
        siteURL: hostname,
        get apiURL() {
            return `${this.siteURL}/api`
        }
    }
}