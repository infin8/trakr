# -*- coding: utf-8 -*-
from collections import defaultdict
from database import db, ObjectId
from datetime import datetime

def campaign_summary(id=None):
    spec = {'campaign':{'$exists':True}}
    exclude =  {'_id':False}
    
    if id: spec['id'] = id
    
    return generate_summary(db.clicks.find(spec, exclude))

def generate_summary(clicks):
    campaigns = defaultdict(lambda: defaultdict(int))
    for click in clicks:
        id = click['campaign']
        campaign = campaigns.get(id, get_campaign(id))                
        campaign['clicks'] += 1
        campaign['leads'] += click.get('leads', 0)
        
        campaigns[id] = campaign
    
    return campaigns.values()

def get_campaign(id=''):
    spec = {'id':id}
    exclude =  {'_id':False}
    
    campaign = db.campaigns.find_one(spec, exclude) if id else None
    
    if campaign: return campaign
    
    campaign = dict(
        id = id,
        name = '',
        payout = 0,
        error = 0,
        clicks = 0,
        leads = 0,
    )
    
    return save_campaign(campaign)

def save_campaign(campaign):
    #todo: sanitize data
    db.campaigns.update({
        'id': campaign['id'],
    }, {
        '$set': campaign
    }, upsert=True)
    
    return campaign
    
def record_click(query={}, ip='', useragent=''):
    query['land_time'] = datetime.utcnow()
    query['ip'] = ip
    query['ua'] = useragent
    
    return str(db.clicks.save(query))

def record_clickthrough(cid, url=''):
    db.clicks.update(
            {'_id': ObjectId(cid), 
            'outbound':{'$exists': False},
            'click_time':{'$exists': False}}, 
            {'$set':{
                'outbound': url,
                'click_time': datetime.utcnow()
            }},
        )

def record_lead(cid):
    try:
        db.clicks.update({'_id':ObjectId(cid)}, {'$set': {'leads': 1}})
        return True
    except:
        return False