jasmine.getFixtures().fixturesPath = '/static/js/jasmine/spec/javascripts/fixtures'
beforeEach(function() {
    loadFixtures('index.html')
    $.fx.off = true;
});

describe("Toasts", function() {
    it("Should be empty by default.", function(){
        expect($(".toast-wrapper")).toBeEmpty()
    })
    it("Should have a message and be visible.", function(){
        toastMessage("success", "whatevs")
        expect($(".toast-wrapper")).toContainElement(`div.toast`)
        expect($(".toast-wrapper")).toBeVisible()
    })
})

describe("Newsletter form function", function() {
    it("Should prevent submit, disable the button and fire the singup method", function(){
        spyEvent = spyOnEvent("#news-form", "submit")
        $("#news-form").on("submit", function (ev) {ev.preventDefault(); 
        $("#news-submit").prop("disabled", true).addClass("disabled");
        const formData = new FormData(this); const formUrl = this.action;
        newsletterSignup(formData, formUrl);})
        spyOn(window, 'newsletterSignup')
        $("#news-submit").trigger("submit")

        expect($("#news-submit")).toBeDisabled()
        expect($("#news-submit")).toHaveClass("disabled")
        expect("submit").toHaveBeenPreventedOn("#news-form")
        expect(spyEvent).toHaveBeenPrevented()
    })
})

// describe("newsletterSignup", function() {
//     it("Should respond with an ajax function", function(){
//         newsletterSignup({"email": "test@test.com"}, "/contact/f/newsletter/") 
//         expect($("#news-submit")).toContainElement(`object`)
//         })
// })