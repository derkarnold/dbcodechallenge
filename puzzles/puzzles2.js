function doFetch(number) {
    return fetch(`840edd20-54c9-4cab-a905-cf8dceebd7d4/call?number=${number}`)
}

function chainedFetch(number) {
    return doFetch(number)
        .then(res => res.json())
        .then(data => chainedFetch(data))
        .catch(error => doFetch(number)
            .then(res => res.text())
            .then(data => { console.log(data) }));
}

chainedFetch(75407395)