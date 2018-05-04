import gzip
import boto3
import json

firehose = boto3.client('firehose',region_name='us-east-1')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    #Get bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    #Get object key
    object = event['Records'][0]['s3']['object']['key']
    
    #Get filename
    filename = object.split('/')[-1]
    #Create file path in lambda
    filepath = '/tmp/'+filename
    s3.meta.client.download_file(bucket, object, filepath)
    
    with gzip.open(filepath,'rb') as file:
        for line in file:
            if line.startswith('#') == False:
                linelist = line.split()
                data={'date':linelist[0],'time':linelist[1],'x_edge_location':linelist[2],\
                    'sc_bytes':linelist[3],'c_ip':linelist[4],'cs_method':linelist[5],\
                    'host':linelist[6],'cs_uri_stem':linelist[7],'sc_status':linelist[8],\
                    'referer':linelist[9],'user_agent':linelist[10],'cs_uri_query':linelist[11],\
                    'cookie':linelist[12],'x_edge_result_type':linelist[13],'x_edge_request_id':linelist[14],\
                    'x_host_header':linelist[15],'cs_protocol':linelist[16],'cs_bytes':linelist[17],\
                    'time_taken':linelist[18],'x_forwarded_for':linelist[19],'ssl_protocol':linelist[20],\
                    'ssl_cipher':linelist[21],'x_edge_response_result_type':linelist[22],\
                    'cs_protocol_version':linelist[23],'fle_status':linelist[24],\
                    'fle_encrypted_fields':linelist[25],'timestamp':linelist[0]+' '+linelist[1]}
                jsondata=json.dumps(data)
                #separator = '|'
                #data = separator.join(linelist)
                #data = data+'\n'
                #jsondata2 = jsondata+'\n'
                print jsondata
                response = firehose.put_record(
                    DeliveryStreamName='cflogs2es',
                    Record={
                        'Data': jsondata
                        }
                )
                print response
