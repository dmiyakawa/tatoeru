# -*- coding=utf-8 -*-
from __future__ import print_function

import logging

import os.path
from os.path import dirname

from models import Post, Reply

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

NAMESPACE = os.path.basename(dirname(os.path.abspath(__file__)))

logger = logging.getLogger('default')

def home(request):
    user = request.user
    if user.is_anonymous():
        logger.debug('home(). Anonymous User')
    else:
        logger.debug('home(). user.email: {}'.format(user.email))

    posts = Post.objects.all()

    lst = []
    for post in posts:
        replies = Reply.objects.filter(post=post)
        lst.append({ 'post_id': post.id,
                     'post_theme': post.theme,
                     'replies': replies })

    return render(request, '{}/home.djhtml'.format(NAMESPACE),
                  { 'lst': lst })


@login_required
def error(request):
    user = request.user
    logger.debug('error(). user.email: {}'.format(user.email))
    return render(request, '{}/error.djhtml'.format(NAMESPACE))


@login_required
def motomeru(request):
    user = request.user
    logger.debug('motomeru(). user.email: {}'.format(user.email))
    return render(request, '{}/motomeru.djhtml'.format(NAMESPACE))


@login_required
def send_motomeru_request(request):
    user = request.user
    logger.debug('send_motomeru_motomeru(). user.email: {}'
                 .format(user.email))
    theme = request.POST['theme']
    if not theme:
        logger.error('No theme provided')
        return redirect('tatoeru_core:error')

    if Post.objects.filter(theme=theme):
        logger.error('The exactly same theme already exists')
        return redirect('tatoeru_core:error')
               
    post = Post.objects.create(user=request.user,
                               theme=theme)
    logger.debug(post)
    return redirect('tatoeru_core:home')


@login_required
def kotaeru(request, post_id):
    user = request.user
    logger.debug('kotaeru(): user.email: {}, post_id: {}'
                 .format(user.email, post_id))

    lst = Post.objects.filter(id=post_id)
    if len(lst) < 1:
        logger.error('Unknown post_id {}'.format(post_id))
        return redirect('tatoeru_core:error')
    post = lst[0]

    return render(request, '{}/kotaeru.djhtml'.format(NAMESPACE),
                  { 'post_id': post.id,
                    'post_theme': post.theme })


@login_required
def send_kotaeru_request(request):
    user = request.user
    post_id = request.POST['post_id']
    tatoe = request.POST['tatoe']
    logger.debug(
        'send_kotaeru_request(). user.email: {}. post_id: {}, tatoe: {}'
        .format(user.email, post_id, tatoe))

    lst = Post.objects.filter(id=post_id)
    if len(lst) < 1:
        logger.error('Unknown post_id {}'.format(post_id))
        return redirect('tatoeru_core:error')
    post = lst[0]

    reply = Reply.objects.create(user=request.user, post=post, tatoe=tatoe)
    logger.debug('post: {}, reply={}'.format(post, reply))

    return redirect('tatoeru_core:home')
