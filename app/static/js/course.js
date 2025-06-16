document.addEventListener("DOMContentLoaded", () => {
  // Part 1: Redirect to course details on button click
  const goToCourseDetail = (button) => {
    const courseId = button.closest('.course_card').getAttribute("data-course-id");
    window.location.href = `/course-detail.html?courseId=${courseId}`;
  };

  // Simulated course data (could be fetched from a database or API)
  const courses = {
    1: {
      title: "HTML & CSS",
      description: `
        <span style="color: #d9534f;">1. Waa maxay HTML & CSS?</span> <br><br>
        HTML (HyperText Markup Language) iyo CSS (Cascading Style Sheets) waa laba ka mid ah luuqadaha ugu muhiimsan ee lagu sameeyo bogagga internetka. HTML waxay u ogolaataa dadka inay abuuraan qaab-dhismeedka bogga, sida qaybo, sawirro, iyo qoraallo. CSS waxay u ogolaataa inay bogga ku qurxiyaan, sida in lagu daro midabada, qaababka, iyo qaab-dhismeedka bogga. Koorsadani waxay diiradda saaraysaa sidii aad u baran lahayd isticmaalka labadaas luuqadood si aad u dhisto bogag internet ah oo la jaanqaadi kara qalabyo kala duwan sida desktop iyo mobile.<br><br>
          
        <span style="color: #d9534f;">2. Maxaad ka baran doontaa?</span> <br><br>
        Inta lagu jiro koorsadan, waxaad baran doontaa sida loo isticmaalo HTML si aad u dhisto boggaga aasaasiga ah, oo ay ku jiraan headings, paragraphs, links, iyo images. Waxaad sidoo kale baran doontaa sida loo isticmaalo CSS si aad u qurxiso muuqaalka boggaada, iyadoo la isticmaalayo midabyo, fonts, iyo qaab-dhismeedyo kala duwan. Koorsadani waxay sidoo kale ku siin doontaa xirfado aad ugu baahan tahay naqshadaynta boggaga responsiv ah, kuwaas oo si fudud ugu shaqeeya qalabyo kala duwan sida telefoonada gacanta iyo laptops.<br><br>
          
        <span style="color: #d9534f;">3. Shuruudaha iyo Faa’iidooyinka Koorsada</span> <br><br>
        Koorsadan waxay ku habboon tahay qof kasta oo raba inuu barto web development, gaar ahaan kuwa doonaya inay noqdaan naqshadeeyayaal web. Waxaad baran doontaa xirfadaha aasaasiga ah ee lagama maarmaanka u ah in lagu sameeyo boggaga internet, kuwaas oo muhiim u ah xirfadaha maanta loo baahan yahay. Koorsada kadib, waxaad heli doontaa shahaado caddeynaysa inaad dhammeystirtay koorsada, taasoo kaa caawin karta inaad si fudud u hesho shaqooyin ku saabsan web development ama inaad bilaawdo mashruucaaga gaarka ah.
      `,
      topics: ["Introduction to HTML", "Styling with CSS", "Responsive Design"],
      videos: [
        { title: "HTML Basics", url: "https://example.com/html-basics", locked: false },
        { title: "CSS Basics", url: "https://example.com/css-basics", locked: false }
      ]
    },
    2: {
      title: "Bootstrap",
      description: `<span style="color: #d9534f;">Waa maxay Bootstrap?</span><br><br>
      Bootstrap waa framework CSS ah oo loo isticmaalo in lagu dhiso websaydyo responsiv ah oo degdeg ah. Waxa uu bixiyaa qaybo horey loo dhisay sida badhamada, menus, iyo grids.<br><br>

      Maxaad ka baran doontaa?<br><br>
      
      Waxaad baran doontaa sida loo isticmaalo Bootstrap si aad u dhisto websaydyo soo jiidasho leh oo ka shaqeeya qalabyo kala duwan sida telefoonada, tablet-yada, iyo desktop-ka.

      
      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     3: {
      title: "JavaScript",
      description: `<span style="color: #d9534f;">Waa maxay JavaScript?</span><br><br>
      JavaScript waa luuqad barnaamijyo ah oo aad u muhiim ah oo loo isticmaalo in lagu daro isdhexgal iyo falgal bogagga internetka. Waxaa loo isticmaalaa si loo sameeyo bogag internet oo firfircoon, sida kuwa leh badhamo gujin kara ama xog dib-u-cusbooneysiin kara.

     <span style="color: #d9534f;"> Maxaad ka baran doontaa? </span><br><br>
      
      Koorsadan, waxaad baran doontaa sida loo abuuro bogag internet oo ka falcelin kara ficillada isticmaalaha. Waxaad baran doontaa xog ururinta, shuruudaha, iyo sida loo isticmaalo JavaScript si loo abuuro bogag isdhexgal leh.

      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     4: {
      title: "Python",
      description:  `<span style="color: #d9534f;">Waa maxay Python?</span><br><br>

      Python waa luuqad barnaamijyo ah oo la isticmaalay si ballaaran. Waxaa loogu talagalay in lagu qoro barnaamijyo fudud iyo kuwa adag, gaar ahaan barashada mashiinka iyo xog ururinta.


      <span style="color: #d9534f;">Maxaad ka baran doontaa?</span><br><br>
      
      Waxaad baran doontaa sida loo isticmaalo Python si loo dhiso barnaamijyo fudud iyo kuwa heer sare ah. Koorsadu waxay kaa caawin doontaa inaad barato farsamooyinka loo isticmaalo barashada mashiinka, xog ururinta, iyo barnaamijyada webka.


      .`,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     5: {
      title: "Flask",
      description: `<span style="color: #d9534f;">Waa maxay Flask?</span><br><br>
      Flask waa micro-framework loo isticmaalo Python si loo dhiso web applications. Waa mid aad u fudud oo loo isticmaalo si degdeg ah loogu dhiso APIs iyo boggaga internetka.

      <span style="color: #d9534f;">Maxaad ka baran doontaa?</span><br><br>
      Waxaad baran doontaa sida loo isticmaalo Flask si aad u dhisto web apps fudud iyo APIs. Koorsada waxay sidoo kale ku tusi doontaa sida loo isticmaalo templates iyo database si loo maareeyo xogta.

      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     6: {
      title: "Mysql",
      description: `<span style="color: #d9534f;">Waa maxay MySQL?</span><br><br>
      MySQL waa database management system (DBMS) oo loo isticmaalo kaydinta xogta. Waxaa si weyn loogu isticmaalaa webka iyo software-yada kala duwan ee u baahan keydinta xogta.

      <span style="color: #d9534f;">Maxaad ka baran doontaa?</span><br><br>
      Waxaad baran doontaa sida loo abuuro databases, loo qoro queries SQL ah si xogta loo raadso ama loo cusboonaysiiyo, iyo sida loo maareeyo xogta si hufan.

       `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     7: {
      title: "figma",
      description: `<span style="color: #d9534f;">Waa maxay Figma?</span><br><br>.
      Figma waa software naqshadeyn oo loogu talagalay sameynta UI/UX designka website, kaas oo u oggolaanaya kooxo kala duwan inay si wadajir ah u shaqeeyaan. Waxaa loo isticmaalaa in lagu abuuro mockups iyo prototypes.

      <span style="color: #d9534f;">Maxaad ka baran doontaa?</span><br><br>
      
      Waxaad baran doontaa sida loo naqshadeeyo interfaces-ka isticmaalaha, mockups, iyo prototypes, iyo sida loo abuuro naqshadeyn wanaagsan oo fudud. Figma waxay si weyn uga caawisaa naqshadeeyayaasha inay ku shaqeeyaan koox ahaan.

      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     8: {
      title: "Adobe Photoshop",
      description: `<span style="color: #d9534f;">Waa maxay Adobe Photoshop? </span><br><br>

      Photoshop waa software-ka ugu caansan ee loogu talagalay tafatirka sawirrada iyo abuurista naqshado farshaxan ah. Waxaa si weyn loogu isticmaalaa naqshadaynta garaafyada, sawirrada, iyo dhejisyada.


      
      <span style="color: #d9534f;">Maxaad ka baran doontaa?</span><br><br>
      Koorsadan waxaad baran doontaa sida loo tafatiro sawirrada, loo sameeyo garaafyo, iyo sida loo abuuro naqshado kala duwan oo loogu talagalay daabacaadda ama webka.


      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    }
    , 9: {
      title: "Adobe Illustrator",
      description: `<span style="color: #d9534f;">Waa maxay Adobe Illustrator?</span><br><br>
      
      
      Illustrator waa software loogu talagalay sameynta naqshado vector-ka ah oo aan wax shucaac kujirin. Waxaa si weyn loogu isticmaalaa naqshadeynta logos, sawirrada vector-ka ah, iyo posterada xayaysiinta.

      Maxaad ka baran doontaa?<br><br>

      Koorsadan, waxaad baran doontaa sida loo abuuro naqshado vector ah oo loo isticmaali karo dhammaan warbaahinta, laga bilaabo calaamadaha ilaa sawirrada waaweyn ee xayaysiinta.

      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     10: {
      title: "Adobe InDesign",
      description: `<span style="color: #d9534f;">Waa maxay Adobe InDesign? </span><br><br>
      
      
      InDesign waa software loogu talagalay naqshadeynta bogagga daabacaadda sida buugaagta, joornaalada, iyo wargeysyada. Waxay sidoo kale u oggolaanaysaa in lagu abuuro naqshado digital ah oo loogu talagalay ebook-yada.

      Maxaad ka baran doontaa?
      
      Waxaad baran doontaa sida loo abuuro dukumiintiyo daabacan, sida buugaagta iyo wargeysyada, iyo sida loo naqshadeeyo layouts-ka boggaga iyo qaybaha kala duwan.

      `,
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    }
    ,
     11: {
      title: "SQL Server",
      description: "Master interactive web development with JavaScript.",
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    },
     12: {
      title: "JavaScript",
      description: "Master interactive web development with JavaScript.",
      topics: ["Variables and Functions", "DOM Manipulation", "ES6 Features"],
      videos: [
        { title: "Variables in JS", url: "https://example.com/js-variables", locked: false },
        { title: "DOM Basics", url: "https://example.com/js-dom", locked: false }
      ]
    }

  };

  // Part 2: Render course details (only for course-detail.html)
  const urlParams = new URLSearchParams(window.location.search);
  const courseId = urlParams.get("courseId");

  if (courseId && document.getElementById("course-title")) {
    const course = courses[courseId];

    if (course) {
      // Update course title and description
      document.getElementById("course-title").textContent = course.title;
      document.getElementById("course-description").innerHTML = course.description;

      // Render topics dynamically
      const topicsList = document.getElementById("course-topics");
      topicsList.innerHTML = ''; // Clear previous content
      course.topics.forEach((topic) => {
        const li = document.createElement("li");
        li.textContent = topic;
        topicsList.appendChild(li);
      });

      // Render videos dynamically
      const videosList = document.getElementById("course-videos");
      videosList.innerHTML = ''; // Clear previous content
      course.videos.forEach((video) => {
        const li = document.createElement("li");
        li.textContent = video.title;

        if (video.locked) {
          li.textContent += " (Locked)";
        } else {
          const a = document.createElement("a");
          a.href = video.url;
          a.textContent = "Watch";
          li.appendChild(a);
        }

        videosList.appendChild(li);
      });
    } else {
      // If no course data exists, display error
      document.getElementById("course-content").textContent = "Course not found.";
    }
  }

  // Part 3: Event Listener for course detail button click
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', () => goToCourseDetail(button));
  });
});
