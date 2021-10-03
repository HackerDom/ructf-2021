const blockGenerate = document.getElementById('block-generate');
const blockListen = document.getElementById('block-listen');
const blockList = document.getElementById('block-list');

const buttonGenerate = document.getElementById('button-generate');
const buttonBack = document.getElementById('button-back');

const elementDescription = document.getElementById('description');
const elementAudio = document.getElementById('audio');
const elementId = document.getElementById('id');


async function apiGenerate(description) {
    return await fetch('/api/generate/', {
        method: 'POST',
        body: description
    }).then(r => r.text());
}

async function apiList() {
    return await fetch('/api/list/', {
        method: 'GET'
    }).then(r => r.json());
}

async function openGenerate() {
    location.hash = '';

    elementAudio.setAttribute('src', '');

    blockListen.hidden = true;
    blockGenerate.hidden = false;
    blockList.hidden = false;
}

async function openListen(id) {
    id = id.replace('#', '');

    location.hash = id;
    elementId.innerText = id;

    elementAudio.setAttribute('src', `/api/listen/${id}/`);

    blockList.hidden = true;
    blockGenerate.hidden = true;
    blockListen.hidden = false;
}

async function createLink(id) {
    const link = document.createElement('div');

    link.className = 'link';
    link.innerText = id;
    link.addEventListener('click', clickLink);

    return link;
}

async function clickGenerate() {
    if (elementDescription.value.length == 0) {
        return;
    }

    const id = await apiGenerate(elementDescription.value);
    const link = await createLink(id);

    blockList.appendChild(link);

    await openListen(id);
    
    elementDescription.value = '';
}

async function clickLink(event) {
    await openListen(event.target.innerText);
}

async function initList() {
    const ids = await apiList();

    for (const id of ids) {
        const link = await createLink(id);

        blockList.appendChild(link);
    }

    blockList.hidden = false;
}

async function init() {
    buttonBack.addEventListener('click', openGenerate);
    buttonGenerate.addEventListener('click', clickGenerate);

    await initList();

    if (location.hash.length > 0) {
        await openListen(location.hash);
    }
    else {
        await openGenerate();
    }
}

init();
