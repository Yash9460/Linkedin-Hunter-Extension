(function() {
  // Extract LinkedIn profile details and send to popup
  function getProfileDetails() {
      // Full Name
      let fullName = document.querySelector('h1.text-heading-xlarge, h1')?.innerText?.trim() || "";
      // Experience section: get current (present) job
      let org = "";
      let designation = "";
      // Find the first experience item with 'Present' in the date
      let expItems = document.querySelectorAll('section#experience-section ul li, .pvs-list__container .pvs-entity, a[data-field="experience_company_logo"]');
      let found = false;
      expItems.forEach(item => {
          let dateText = item.innerText.toLowerCase();
          if (!found && dateText.includes('present')) {
              // Designation
              let titleElem = item.querySelector('div.mr1.hoverable-link-text.t-bold span[aria-hidden="true"]');
              if (titleElem) designation = titleElem.innerText.trim();
              // Organisation
              let orgElem = item.querySelector('span.t-14.t-normal span[aria-hidden="true"]');
              if (orgElem) {
                  let orgText = orgElem.innerText.trim();
                  // Get only the company name before '·'
                  org = orgText.split('·')[0].trim();
              }
              found = true;
          }
      });
      // Fallbacks if not found
      if (!org) {
          let expCompany = document.querySelector('.pv-entity__secondary-title');
          if (expCompany) org = expCompany.innerText.trim();
      }
      if (!designation) {
          designation = document.querySelector('.text-body-medium.break-words')?.innerText?.trim() || "";
      }
      return { fullName, org, designation };
  }

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === "getProfileDetails") {
          sendResponse(getProfileDetails());
      }
  });
})();
