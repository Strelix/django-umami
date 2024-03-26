
??? note
    This is a message from the maintainer and project owner, [`@trey`](https://github.com/TreyWW).

Personally, I use [`Umami`](https://umami.is/) for every project. It allows me to easily see what parts of my sites are most 
used. I chose Umami as they allow self-hosting and are privacy focused - cool right! 
Okay cool... but why did I create `Django-Umami`, and what's the difference?

Well django-umami is a library aimed to help integrate your own umami analytics through your django site. Typically, to use 
Umami you'd use a HTML `#!html <script>` tag with an `#!html data-website-id` that links to your website-id. But this has one 
problem - it's public!? Anyone can use this website ID and fake traffic to your site. This is one major flaw of Umami. I did 
create a security report of this on their Github, but they took no care of it, simply accepting the issue.

So I thought, why not make an easy-to-use backend integration. This way users don't get told your secret key. The only real 
downside to this is that you're backend is making outbound requests and you lose a lot of the user data such as Device Type, 
Screen Size, location, etc etc.

### TLDR

<div class="grid" markdown>
!!! success "Positives"
    - Able to hide secret website-id
    -  Able to customise event names, urls, and any other data 

!!! failure "Negatives"
    -  Your backend will make requests, not the users client. So you'll have higher outbound bandwidth  
    -  You lose some user information, such as device type and screen size
</div>