
export function setLoadingVisibility(visible: boolean) {
    if (visible) {
        $('#loading_mask').removeClass('invisible');
    } else {
        $('#loading_mask').addClass('invisible');
    }
}
