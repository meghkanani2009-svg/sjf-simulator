import streamlit as st
import streamlit.components.v1 as components

# --- 1. Page Configuration ---
st.set_page_config(page_title="Lithos Geology", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Hide Streamlit UI for Full-Screen Effect ---
st.markdown("""
    <style>
        /* Hide top header, footer, and remove all padding */
        [data-testid="stHeader"] { visibility: hidden; }
        footer { visibility: hidden; }
        .block-container { padding: 0 !important; max-width: 100% !important; overflow: hidden !important; }
        
        /* Make the iframe take up the full screen */
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. The Complete HTML/CSS/JS (Translated from React) ---
lithos_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,400;1,500;1,600&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        .font-playfair { font-family: 'Playfair Display', serif; }
        
        @keyframes heroReveal { 0%{opacity:0;transform:translateY(28px);filter:blur(12px)} 100%{opacity:1;transform:translateY(0);filter:blur(0)} }
        @keyframes heroFadeUp { 0%{opacity:0;transform:translateY(20px)} 100%{opacity:1;transform:translateY(0)} }
        @keyframes heroZoom { 0%{transform:scale(1.12)} 100%{transform:scale(1)} }
        
        .hero-anim { opacity:0; animation-fill-mode:forwards; animation-timing-function:cubic-bezier(0.16,1,0.3,1); }
        .hero-reveal { animation-name:heroReveal; animation-duration:1.1s; }
        .hero-fade { animation-name:heroFadeUp; animation-duration:1s; }
        .hero-zoom { animation:heroZoom 1.8s cubic-bezier(0.16,1,0.3,1) forwards; }
        
        @media (prefers-reduced-motion: reduce){ .hero-anim,.hero-zoom{ animation:none; opacity:1; } }
    </style>
</head>
<body class="m-0 p-0 overflow-hidden min-h-screen bg-white tracking-[-0.02em]">

    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-[100] flex items-center justify-between p-4 sm:p-5">
        <div class="flex items-center gap-2 cursor-pointer">
            <svg width="26" height="26" viewBox="0 0 256 256" fill="#ffffff" xmlns="http://www.w3.org/2000/svg">
                <path d="M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z" />
            </svg>
            <span class="text-white text-2xl font-playfair italic">Lithos</span>
        </div>

        <div class="hidden md:flex absolute left-1/2 -translate-x-1/2 bg-white/20 backdrop-blur-md border border-white/30 rounded-full px-2 py-2 items-center gap-1">
            <button class="text-white px-4 py-1.5 rounded-full text-sm font-medium transition-colors hover:bg-white/20">Course</button>
            <button class="text-white/80 px-4 py-1.5 rounded-full text-sm font-medium transition-colors hover:bg-white/20 hover:text-white">Field Guides</button>
            <button class="text-white/80 px-4 py-1.5 rounded-full text-sm font-medium transition-colors hover:bg-white/20 hover:text-white">Geology</button>
            <button class="text-white/80 px-4 py-1.5 rounded-full text-sm font-medium transition-colors hover:bg-white/20 hover:text-white">Plans</button>
            <button class="text-white/80 px-4 py-1.5 rounded-full text-sm font-medium transition-colors hover:bg-white/20 hover:text-white">Live Tour</button>
        </div>

        <div class="flex items-center">
            <button class="hidden md:block bg-white text-gray-900 text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-gray-100 transition-colors">Sign Up</button>
            <button class="md:hidden text-white p-1"><i data-lucide="menu"></i></button>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative w-full overflow-hidden h-screen bg-black" style="height: 100dvh;">
        
        <!-- Base Image -->
        <div class="absolute inset-0 bg-center bg-cover bg-no-repeat z-10 hero-zoom" style="background-image: url('https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_195923_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png&w=1280&q=85')"></div>

        <!-- Canvas for Spotlight generation -->
        <canvas id="maskCanvas" class="absolute inset-0 pointer-events-none" style="display: none;"></canvas>

        <!-- Reveal Layer (Masked Image) -->
        <div id="revealLayer" class="absolute inset-0 bg-center bg-cover bg-no-repeat z-30 pointer-events-none" style="background-image: url('https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_201152_bba90a12-bf12-459f-91f0-51f237dbaf3b.png&w=1280&q=85');"></div>

        <!-- Heading -->
        <div class="absolute top-[14%] left-0 right-0 flex flex-col items-center text-center px-5 pointer-events-none z-50">
            <h1 class="text-white leading-[0.95]">
                <span class="block font-playfair italic font-normal text-5xl sm:text-7xl md:text-8xl hero-anim hero-reveal" style="letter-spacing: -0.05em; animation-delay: 0.25s;">Layers hold</span>
                <span class="block font-normal text-5xl sm:text-7xl md:text-8xl -mt-1 hero-anim hero-reveal" style="letter-spacing: -0.08em; animation-delay: 0.42s;">tales of time</span>
            </h1>
        </div>

        <!-- Bottom Left Text -->
        <div class="hidden sm:block absolute bottom-14 left-10 md:left-14 max-w-[260px] z-50 hero-anim hero-fade" style="animation-delay: 0.7s;">
            <p class="text-sm text-white/80 leading-relaxed drop-shadow-sm">Every layer of sediment records a chapter of our planet, from ancient seabeds to drifting ash, layered across millions of years beneath us.</p>
        </div>

        <!-- Bottom Right Content -->
        <div class="absolute bottom-10 sm:bottom-24 left-5 right-5 sm:left-auto sm:right-10 md:right-14 max-w-full sm:max-w-[260px] flex flex-col items-start gap-4 sm:gap-5 z-50 hero-anim hero-fade" style="animation-delay: 0.85s;">
            <p class="text-xs sm:text-sm text-white/80 leading-relaxed drop-shadow-sm">Our interactive maps let you peel back the crust to trace how stones, fossils, and deep time combine to shape the ground beneath your feet.</p>
            <button class="bg-[#e8702a] hover:bg-[#d2611f] text-white text-sm font-medium px-7 py-3 rounded-full transition-all hover:scale-[1.03] active:scale-95 hover:shadow-lg hover:shadow-[#e8702a]/30">Start Digging</button>
        </div>
    </section>

    <!-- Interactive Spotlight Logic -->
    <script>
        lucide.createIcons(); // Initialize Icons

        const canvas = document.getElementById('maskCanvas');
        const revealLayer = document.getElementById('revealLayer');
        const ctx = canvas.getContext('2d');
        const SPOTLIGHT_R = 260;

        let mouse = { x: -999, y: -999 };
        let smooth = { x: -999, y: -999 };

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
            if (smooth.x === -999) {
                smooth.x = e.clientX;
                smooth.y = e.clientY;
            }
        });

        function animateSpotlight() {
            if (smooth.x !== -999) {
                smooth.x += (mouse.x - smooth.x) * 0.1;
                smooth.y += (mouse.y - smooth.y) * 0.1;

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                const gradient = ctx.createRadialGradient(smooth.x, smooth.y, 0, smooth.x, smooth.y, SPOTLIGHT_R);
                gradient.addColorStop(0, 'rgba(255,255,255,1)');
                gradient.addColorStop(0.4, 'rgba(255,255,255,1)');
                gradient.addColorStop(0.6, 'rgba(255,255,255,0.75)');
                gradient.addColorStop(0.75, 'rgba(255,255,255,0.4)');
                gradient.addColorStop(0.88, 'rgba(255,255,255,0.12)');
                gradient.addColorStop(1, 'rgba(255,255,255,0)');

                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(smooth.x, smooth.y, SPOTLIGHT_R, 0, Math.PI * 2);
                ctx.fill();

                const maskUrl = canvas.toDataURL();
                revealLayer.style.maskImage = `url(${maskUrl})`;
                revealLayer.style.webkitMaskImage = `url(${maskUrl})`;
                revealLayer.style.maskSize = '100% 100%';
                revealLayer.style.webkitMaskSize = '100% 100%';
            }
            requestAnimationFrame(animateSpotlight);
        }
        animateSpotlight();
    </script>
</body>
</html>
"""

# --- 4. Render the Code ---
components.html(lithos_html, height=1000, scrolling=False)
